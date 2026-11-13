"""Business logic shared by the REST API and the server-rendered UI."""
import random
import threading
import time
from typing import Optional

from .db import db
from .pricing import SHIPPING_CENTS, TAX_RATES, price_order
from .security import hash_password

DECLINED_CARD = "4000000000000002"


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


# ---------------------------------------------------------------- users
def register_user(email: str, password: str, tier: str = "standard") -> dict:
    email = email.strip().lower()
    if "@" not in email or len(password) < 6:
        raise ApiError(422, "invalid_input", "Valid email and a password of 6+ characters are required")
    with db() as c:
        if c.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            raise ApiError(409, "email_taken", "Email already registered")
        cur = c.execute(
            "INSERT INTO users(email,password_hash,tier) VALUES(?,?,?)", (email, hash_password(password), tier)
        )
        return {"id": cur.lastrowid, "email": email, "tier": tier}


def authenticate(email: str, password: str) -> dict:
    with db() as c:
        row = c.execute("SELECT * FROM users WHERE email=?", (email.strip().lower(),)).fetchone()
    if not row or row["password_hash"] != hash_password(password):
        raise ApiError(401, "invalid_credentials", "Invalid email or password")
    return dict(row)


def get_user(user_id: int) -> Optional[dict]:
    with db() as c:
        row = c.execute("SELECT id,email,tier FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else None


# ------------------------------------------------------------- products
def list_products(category: Optional[str] = None, q: Optional[str] = None) -> list:
    sql, args = "SELECT * FROM products WHERE 1=1", []
    if category:
        sql += " AND category=?"
        args.append(category)
    if q and q.strip():
        sql += " AND LOWER(name) LIKE ?"
        args.append(f"%{q.strip().lower()}%")
    with db() as c:
        return [dict(r) for r in c.execute(sql + " ORDER BY id", args)]


def get_product(product_id: int) -> dict:
    with db() as c:
        row = c.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not row:
        raise ApiError(404, "not_found", "Product not found")
    return dict(row)


def create_product(sku: str, name: str, category: str, price_cents: int, stock: int) -> dict:
    with db() as c:
        if c.execute("SELECT 1 FROM products WHERE sku=?", (sku,)).fetchone():
            raise ApiError(409, "sku_taken", "SKU already exists")
        cur = c.execute(
            "INSERT INTO products(sku,name,category,price_cents,stock) VALUES(?,?,?,?,?)",
            (sku, name, category, price_cents, stock),
        )
    return get_product(cur.lastrowid)


def set_stock(product_id: int, stock: int) -> dict:
    with db() as c:
        c.execute("UPDATE products SET stock=? WHERE id=?", (stock, product_id))
    return get_product(product_id)


# ----------------------------------------------------------------- cart
def cart_lines(user_id: int) -> list:
    with db() as c:
        rows = c.execute(
            """SELECT p.id product_id, p.sku, p.name, p.price_cents, p.stock, ci.qty
               FROM cart_items ci JOIN products p ON p.id=ci.product_id
               WHERE ci.user_id=? ORDER BY p.id""",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def add_to_cart(user_id: int, product_id: int, qty: int) -> list:
    if qty < 1 or qty > 20:
        raise ApiError(422, "invalid_quantity", "Quantity must be between 1 and 20")
    product = get_product(product_id)
    with db() as c:
        existing = c.execute(
            "SELECT qty FROM cart_items WHERE user_id=? AND product_id=?", (user_id, product_id)
        ).fetchone()
        new_qty = qty + (existing["qty"] if existing else 0)
        if new_qty > product["stock"]:
            raise ApiError(409, "insufficient_stock", f"Only {product['stock']} in stock")
        c.execute(
            "INSERT INTO cart_items(user_id,product_id,qty) VALUES(?,?,?) "
            "ON CONFLICT(user_id,product_id) DO UPDATE SET qty=excluded.qty",
            (user_id, product_id, new_qty),
        )
    return cart_lines(user_id)


def remove_from_cart(user_id: int, product_id: int) -> list:
    with db() as c:
        c.execute("DELETE FROM cart_items WHERE user_id=? AND product_id=?", (user_id, product_id))
    return cart_lines(user_id)


# ------------------------------------------------------------- checkout
def get_coupon(code: Optional[str]) -> Optional[dict]:
    if not code:
        return None
    with db() as c:
        row = c.execute("SELECT * FROM coupons WHERE code=?", (code.strip().upper(),)).fetchone()
    if not row:
        raise ApiError(422, "invalid_coupon", "Unknown coupon code")
    coupon = dict(row)
    if coupon["used"] >= coupon["max_uses"]:
        raise ApiError(422, "coupon_exhausted", "Coupon usage limit reached")
    return coupon


def quote(user_id: int, region: str, shipping_method: str, coupon_code: Optional[str]) -> dict:
    if region not in TAX_RATES:
        raise ApiError(422, "invalid_region", f"Region must be one of {sorted(TAX_RATES)}")
    if shipping_method not in SHIPPING_CENTS:
        raise ApiError(422, "invalid_shipping", f"Shipping must be one of {sorted(SHIPPING_CENTS)}")
    lines = cart_lines(user_id)
    if not lines:
        raise ApiError(422, "empty_cart", "Cart is empty")
    for l in lines:
        if l["qty"] > l["stock"]:
            raise ApiError(409, "insufficient_stock", f"{l['name']} is out of stock")
    user = get_user(user_id)
    coupon = get_coupon(coupon_code)
    pricing = price_order([(l["price_cents"], l["qty"]) for l in lines], region, shipping_method, user["tier"], coupon)
    return {"lines": lines, "coupon": coupon_code.upper() if coupon_code else None, **pricing}


def checkout(user_id: int, region: str, shipping_method: str, coupon_code: Optional[str], card_number: str) -> dict:
    q = quote(user_id, region, shipping_method, coupon_code)
    card = (card_number or "").replace(" ", "")
    if len(card) != 16 or not card.isdigit():
        raise ApiError(422, "invalid_card", "Card number must be 16 digits")
    _fraud_screen(card)

    with db() as c:
        c.execute("BEGIN IMMEDIATE")
        try:
            # availability is already validated in quote(); just reserve
            for line in q["lines"]:
                c.execute("UPDATE products SET stock=stock-? WHERE id=?", (line["qty"], line["product_id"]))
            if q["coupon"]:
                cur = c.execute(
                    "UPDATE coupons SET used=used+1 WHERE code=? AND used<max_uses", (q["coupon"],)
                )
                if cur.rowcount == 0:
                    raise ApiError(422, "coupon_exhausted", "Coupon usage limit reached")
            cur = c.execute(
                """INSERT INTO orders(user_id,status,region,shipping_method,coupon_code,subtotal_cents,
                   discount_cents,tax_cents,shipping_cents,total_cents) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (user_id, "PENDING", region, shipping_method, q["coupon"], q["subtotal_cents"],
                 q["discount_cents"], q["tax_cents"], q["shipping_cents"], q["total_cents"]),
            )
            order_id = cur.lastrowid
            c.executemany(
                "INSERT INTO order_items(order_id,product_id,sku,name,qty,unit_price_cents) VALUES(?,?,?,?,?,?)",
                [(order_id, l["product_id"], l["sku"], l["name"], l["qty"], l["price_cents"]) for l in q["lines"]],
            )
            c.execute("DELETE FROM cart_items WHERE user_id=?", (user_id,))
            c.execute("COMMIT")
        except Exception:
            c.execute("ROLLBACK")
            raise

    _charge_card(order_id, card)
    _queue_confirmation(order_id)
    return get_order(order_id, user_id)


def _queue_confirmation(order_id: int) -> None:
    """Hand the order to the notification queue (mock broker round-trip)."""
    time.sleep(0.12)
    with db() as c:
        c.execute("UPDATE orders SET status='PENDING' WHERE id=?", (order_id,))


def _fraud_screen(card: str) -> None:
    """Mock call to the fraud-screening provider (network latency)."""
    time.sleep(0.05)


def _charge_card(order_id: int, card: str) -> None:
    """Mock payment gateway: reports the result asynchronously via a webhook-style event."""
    event = "payment.failed" if card == DECLINED_CARD else "payment.succeeded"
    delay = random.uniform(0.05, 0.25)
    threading.Timer(delay, apply_payment_event, args=(order_id, event, f"pay_{order_id}_{card[-4:]}")).start()


def apply_payment_event(order_id: int, event: str, payment_ref: str) -> None:
    with db() as c:
        order = c.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        if not order or order["status"] != "PENDING":
            return  # idempotent: ignore duplicates / late events
        if event == "payment.succeeded":
            c.execute("UPDATE orders SET status='PAID', payment_ref=? WHERE id=?", (payment_ref, order_id))
            _notify(c, order["user_id"], f"Order #{order_id} confirmed", "Thanks for your purchase!")
        elif event == "payment.failed":
            c.execute("UPDATE orders SET status='PAYMENT_FAILED', payment_ref=? WHERE id=?", (payment_ref, order_id))
            _restock(c, order_id)
            _notify(c, order["user_id"], f"Payment failed for order #{order_id}", "Your card was declined.")


def _restock(c, order_id: int) -> None:
    for item in c.execute("SELECT product_id, qty FROM order_items WHERE order_id=?", (order_id,)).fetchall():
        c.execute("UPDATE products SET stock=stock+? WHERE id=?", (item["qty"], item["product_id"]))


def _notify(c, user_id: int, subject: str, body: str) -> None:
    user = c.execute("SELECT email FROM users WHERE id=?", (user_id,)).fetchone()
    c.execute("INSERT INTO outbox(to_email,subject,body) VALUES(?,?,?)", (user["email"], subject, body))


# --------------------------------------------------------------- orders
def get_order(order_id: int, user_id: Optional[int] = None) -> dict:
    with db() as c:
        order = c.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        if not order or (user_id is not None and order["user_id"] != user_id):
            raise ApiError(404, "not_found", "Order not found")
        items = c.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,)).fetchall()
    return {**dict(order), "items": [dict(i) for i in items]}


def list_orders(user_id: int) -> list:
    with db() as c:
        ids = [r["id"] for r in c.execute("SELECT id FROM orders WHERE user_id=? ORDER BY id DESC", (user_id,))]
    return [get_order(i, user_id) for i in ids]


def cancel_order(order_id: int, user_id: int) -> dict:
    order = get_order(order_id, user_id)
    if order["status"] not in ("PENDING", "PAID"):
        raise ApiError(409, "invalid_state", f"Cannot cancel an order in status {order['status']}")
    with db() as c:
        c.execute("UPDATE orders SET status='CANCELLED' WHERE id=?", (order_id,))
        _restock(c, order_id)
        _notify(c, user_id, f"Order #{order_id} cancelled", "Your order was cancelled.")
    return get_order(order_id, user_id)


def refund_order(order_id: int, user_id: int) -> dict:
    order = get_order(order_id, user_id)
    if order["status"] != "PAID":
        raise ApiError(409, "invalid_state", "Only PAID orders can be refunded")
    with db() as c:
        c.execute("UPDATE orders SET status='REFUNDED' WHERE id=?", (order_id,))
        _restock(c, order_id)
        _notify(c, user_id, f"Refund issued for order #{order_id}", f"Refunded {order['total_cents']} cents.")
    return get_order(order_id, user_id)

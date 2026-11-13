from typing import Optional

from fastapi import APIRouter, Depends, Header, Request
from pydantic import BaseModel

from . import services as svc
from .config import ADMIN_KEY, TEST_MODE, WEBHOOK_SECRET
from .db import db, init_db
from .security import create_token, verify_token

router = APIRouter(prefix="/api")


# ----------------------------------------------------------------- auth
def current_user(request: Request, authorization: Optional[str] = Header(None)) -> dict:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    token = token or request.cookies.get("token")
    user_id = verify_token(token) if token else None
    user = svc.get_user(user_id) if user_id else None
    if not user:
        raise svc.ApiError(401, "unauthorized", "Missing, invalid or expired token")
    return user


def require_admin(x_admin_key: Optional[str] = Header(None)) -> None:
    if x_admin_key != ADMIN_KEY:
        raise svc.ApiError(403, "forbidden", "Admin key required")


class Credentials(BaseModel):
    email: str
    password: str


class CartItem(BaseModel):
    product_id: int
    qty: int = 1


class CheckoutRequest(BaseModel):
    region: str = "IN"
    shipping_method: str = "standard"
    coupon_code: Optional[str] = None
    card_number: str = ""


class QuoteRequest(BaseModel):
    region: str = "IN"
    shipping_method: str = "standard"
    coupon_code: Optional[str] = None


class NewProduct(BaseModel):
    sku: str
    name: str
    category: str
    price_cents: int
    stock: int


class StockUpdate(BaseModel):
    stock: int


class TierUpdate(BaseModel):
    email: str
    tier: str


class PaymentEvent(BaseModel):
    order_id: int
    event: str
    payment_ref: str = "evt_manual"


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/auth/register", status_code=201)
def register(body: Credentials):
    return svc.register_user(body.email, body.password)


@router.post("/auth/login")
def login(body: Credentials):
    user = svc.authenticate(body.email, body.password)
    return {"token": create_token(user["id"]), "token_type": "bearer", "user": {"id": user["id"], "email": user["email"], "tier": user["tier"]}}


@router.get("/me")
def me(user: dict = Depends(current_user)):
    return user


# ------------------------------------------------------------- products
@router.get("/products")
def products(category: Optional[str] = None, q: Optional[str] = None):
    return svc.list_products(category, q)


@router.get("/products/{product_id}")
def product(product_id: int):
    return svc.get_product(product_id)


# ----------------------------------------------------------------- cart
@router.get("/cart")
def get_cart(user: dict = Depends(current_user)):
    return {"lines": svc.cart_lines(user["id"])}


@router.post("/cart/items", status_code=201)
def add_cart_item(body: CartItem, user: dict = Depends(current_user)):
    return {"lines": svc.add_to_cart(user["id"], body.product_id, body.qty)}


@router.delete("/cart/items/{product_id}")
def delete_cart_item(product_id: int, user: dict = Depends(current_user)):
    return {"lines": svc.remove_from_cart(user["id"], product_id)}


# ------------------------------------------------------------- checkout
@router.post("/checkout/quote")
def checkout_quote(body: QuoteRequest, user: dict = Depends(current_user)):
    return svc.quote(user["id"], body.region, body.shipping_method, body.coupon_code)


@router.post("/checkout", status_code=201)
def do_checkout(body: CheckoutRequest, user: dict = Depends(current_user)):
    return svc.checkout(user["id"], body.region, body.shipping_method, body.coupon_code, body.card_number)


# --------------------------------------------------------------- orders
@router.get("/orders")
def orders(user: dict = Depends(current_user)):
    return svc.list_orders(user["id"])


@router.get("/orders/{order_id}")
def order(order_id: int, user: dict = Depends(current_user)):
    return svc.get_order(order_id, user["id"])


@router.post("/orders/{order_id}/cancel")
def cancel(order_id: int, user: dict = Depends(current_user)):
    return svc.cancel_order(order_id, user["id"])


@router.post("/orders/{order_id}/refund")
def refund(order_id: int, user: dict = Depends(current_user)):
    return svc.refund_order(order_id, user["id"])


# ------------------------------------------------------------- webhooks
@router.post("/webhooks/payment", status_code=202)
def payment_webhook(body: PaymentEvent, x_webhook_secret: Optional[str] = Header(None)):
    if x_webhook_secret != WEBHOOK_SECRET:
        raise svc.ApiError(401, "bad_signature", "Invalid webhook secret")
    svc.apply_payment_event(body.order_id, body.event, body.payment_ref)
    return {"accepted": True}


# ---------------------------------------------------------------- admin
@router.post("/admin/products", status_code=201, dependencies=[Depends(require_admin)])
def admin_create_product(body: NewProduct):
    return svc.create_product(body.sku, body.name, body.category, body.price_cents, body.stock)


@router.patch("/admin/products/{product_id}/stock", dependencies=[Depends(require_admin)])
def admin_set_stock(product_id: int, body: StockUpdate):
    return svc.set_stock(product_id, body.stock)


@router.post("/admin/users/tier", dependencies=[Depends(require_admin)])
def admin_set_tier(body: TierUpdate):
    if body.tier not in ("standard", "gold"):
        raise svc.ApiError(422, "invalid_tier", "Tier must be standard or gold")
    with db() as c:
        cur = c.execute("UPDATE users SET tier=? WHERE email=?", (body.tier, body.email.lower()))
        if cur.rowcount == 0:
            raise svc.ApiError(404, "not_found", "User not found")
    return {"email": body.email.lower(), "tier": body.tier}


# ----------------------------------------------- test helpers (TEST_MODE)
if TEST_MODE:

    @router.get("/_test/outbox")
    def outbox(to: Optional[str] = None):
        sql, args = "SELECT * FROM outbox", []
        if to:
            sql += " WHERE to_email=?"
            args.append(to.lower())
        with db() as c:
            return [dict(r) for r in c.execute(sql + " ORDER BY id", args)]

    @router.post("/_test/reset", dependencies=[Depends(require_admin)])
    def reset():
        init_db(reset=True)
        return {"reset": True}

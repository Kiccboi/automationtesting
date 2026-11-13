import sqlite3
from contextlib import contextmanager
from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  tier TEXT NOT NULL DEFAULT 'standard'      -- standard | gold
);
CREATE TABLE IF NOT EXISTS products(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price_cents INTEGER NOT NULL,
  stock INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS cart_items(
  user_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty INTEGER NOT NULL,
  PRIMARY KEY(user_id, product_id)
);
CREATE TABLE IF NOT EXISTS coupons(
  code TEXT PRIMARY KEY,
  kind TEXT NOT NULL,                        -- percent | flat | freeship
  value INTEGER NOT NULL DEFAULT 0,
  min_subtotal_cents INTEGER NOT NULL DEFAULT 0,
  max_uses INTEGER NOT NULL DEFAULT 1000,
  used INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS orders(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  status TEXT NOT NULL,                      -- PENDING | PAID | PAYMENT_FAILED | CANCELLED | REFUNDED
  region TEXT NOT NULL,
  shipping_method TEXT NOT NULL,
  coupon_code TEXT,
  subtotal_cents INTEGER NOT NULL,
  discount_cents INTEGER NOT NULL,
  tax_cents INTEGER NOT NULL,
  shipping_cents INTEGER NOT NULL,
  total_cents INTEGER NOT NULL,
  payment_ref TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS order_items(
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  sku TEXT NOT NULL,
  name TEXT NOT NULL,
  qty INTEGER NOT NULL,
  unit_price_cents INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS outbox(            -- mock email/notification sink
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  to_email TEXT NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_PRODUCTS = [
    ("KB-100", "Mechanical Keyboard", "peripherals", 8999, 25),
    ("MS-200", "Wireless Mouse", "peripherals", 2499, 40),
    ("MN-300", "27-inch Monitor", "displays", 21999, 10),
    ("HD-400", "USB-C Hub", "accessories", 3499, 60),
    ("WC-500", "HD Webcam", "peripherals", 4599, 15),
    ("CH-600", "Ergonomic Chair", "furniture", 15999, 5),
    ("LP-700", "Laptop Stand", "accessories", 1999, 80),
    ("RARE-1", "Limited Edition Desk Mat", "accessories", 5999, 1),
]
SEED_COUPONS = [
    ("SAVE10", "percent", 10, 0, 1000),
    ("FLAT5", "flat", 500, 2000, 1000),
    ("FREESHIP", "freeship", 0, 5000, 1000),
    ("ONCE", "percent", 20, 0, 1),
]


def connect():
    conn = sqlite3.connect(DB_PATH, timeout=10, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def db():
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()


def init_db(reset: bool = False):
    with db() as c:
        if reset:
            for t in ("users", "products", "cart_items", "coupons", "orders", "order_items", "outbox"):
                c.execute(f"DROP TABLE IF EXISTS {t}")
        c.executescript(SCHEMA)
        if c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            c.executemany(
                "INSERT INTO products(sku,name,category,price_cents,stock) VALUES(?,?,?,?,?)", SEED_PRODUCTS
            )
        if c.execute("SELECT COUNT(*) FROM coupons").fetchone()[0] == 0:
            c.executemany(
                "INSERT INTO coupons(code,kind,value,min_subtotal_cents,max_uses) VALUES(?,?,?,?,?)", SEED_COUPONS
            )

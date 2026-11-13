import os

DB_PATH = os.getenv("SHOPFLOW_DB", os.path.join(os.path.dirname(__file__), "..", "data", "shopflow.db"))
SECRET = os.getenv("SHOPFLOW_SECRET", "dev-secret-change-me")
ADMIN_KEY = os.getenv("SHOPFLOW_ADMIN_KEY", "admin-key")
WEBHOOK_SECRET = os.getenv("SHOPFLOW_WEBHOOK_SECRET", "whsec_test")
TOKEN_TTL_SECONDS = int(os.getenv("SHOPFLOW_TOKEN_TTL", "3600"))
# When true, /api/_test/* helper endpoints are mounted (never enable in prod).
TEST_MODE = os.getenv("SHOPFLOW_TEST_MODE", "1") == "1"

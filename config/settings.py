
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

ADMIN_URL = os.getenv(
    "ADMIN_URL",
    f"{BASE_URL}/admin/"
)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

TIMEOUT = int(os.getenv("TIMEOUT", "10"))

PARENT_PAGE_ID = os.getenv("PARENT_PAGE_ID", "60")

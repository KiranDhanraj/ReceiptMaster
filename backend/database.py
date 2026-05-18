from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
load_dotenv()
from sqlalchemy.engine import URL
import os

# Example: store these in .env
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DATABASE_URL = URL.create(
    "postgresql",
    username="postgres",
    password=DB_PASSWORD,
    host="localhost",
    database="receipt_app",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("DB connection OK")
except Exception as exc:
    print(f"DB connection failed: {exc}")
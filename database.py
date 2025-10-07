from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")

DATABASE_URL = os.getenv(f"DATABASE_URL_{ENV.upper()}")

print("database ENV:", ENV)
print("database DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

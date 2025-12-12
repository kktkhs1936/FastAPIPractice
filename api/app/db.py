import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:secretpassword@db:5432/appdb")

engine = create_engine(DATABASE_URL, echo=True)  # echo=True だと SQL がログ出力される

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# FastAPI で使う Session 依存関係
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

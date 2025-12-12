from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, db

import os
import glob

# 初回起動時にテーブルを自動作成（本番は Alembic 推奨）
db.Base.metadata.create_all(bind=db.engine)

description = """
TestApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.
"""
app = FastAPI(
  title="TestApp",
  description=description,
  summary="Deadpool's favorite app. Nuff said.",
  version="0.0.1",
)


@app.get("/", tags=["root"])
def read_root():
  return {"message": "FastAPI + PostgreSQL on Docker"}

@app.get("/test", tags=["test"])
def get_test():
  return {"message": "test!"}

@app.get("/test/pwd", tags=["test"])
def get_pwd():
  path = os.getcwd()
  return {"message": path}


@app.post("/items", response_model=schemas.ItemRead, tags=["item"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(db.get_db)):
  db_item = models.Item(name=item.name, description=item.description)
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item


@app.get("/items/{item_id}", response_model=schemas.ItemRead, tags=["item"])
def read_item(item_id: int, db: Session = Depends(db.get_db)):
  db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
  if not db_item:
      raise HTTPException(status_code=404, detail="Item not found")
  return db_item


@app.get("/items", response_model=list[schemas.ItemRead], tags=["item"])
def list_items(db: Session = Depends(db.get_db)):
  items = db.query(models.Item).all()
  return items

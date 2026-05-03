"""
Codex Dojo - FastAPI 앱 (의도적 버그 포함)
Level 1, 2 실습용. Codex가 버그를 찾아 수정해야 함.
"""
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import TAX_RATE

app = FastAPI(title="Codex Dojo API")

items_db = {}

class Item(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: str
    name: str
    price: float
    tax: Optional[float] = None

@app.get("/")
def root():
    return {"message": "Welcome to Codex Dojo API"}

@app.post("/items")
def create_item(item: Item):
    new_id = str(uuid4())
    tax = item.price * TAX_RATE
    items_db[new_id] = {**item.model_dump(), "tax": tax}
    return ItemResponse(id=new_id, name=item.name, price=item.price, tax=tax)

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id]}

@app.get("/items")
def list_items():
    return list(items_db.values())

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Deleted"}

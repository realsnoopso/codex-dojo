"""
Codex Dojo - FastAPI 앱 (의도적 버그 포함)
Level 1, 2 실습용. Codex가 버그를 찾아 수정해야 함.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import calculate_total, format_response

app = FastAPI(title="Codex Dojo API")

# 버그 1: 빈 in-memory DB, concurrent access unsafe
items_db = {}

class Item(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    tax: float = None  # 버그 2: Optional 아닌데 None 기본값

@app.get("/")
def root():
    return {"message": "Welcome to Codex Dojo API"}

@app.post("/items")
def create_item(item: Item):
    # 버그 3: ID 생성 방식이 취약 (중복 가능성)
    new_id = len(items_db) + 1
    items_db[new_id] = item.dict()
    # 버그 4: tax 계산 로직 누락
    return ItemResponse(id=new_id, name=item.name, price=item.price)

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # 버그 5: KeyError 대신 적절한 404 처리 필요
    item = items_db[item_id]
    return item

@app.get("/items")
def list_items():
    return list(items_db.values())

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Deleted"}

# 버그 6: 의도된 SyntaxError — 아래 라인 주석 처리되어 함수 정의 안 끝남
# def broken_function(
#     print("이건 실행되면 안됨")

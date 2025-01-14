from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

all_items = []

@app.get("/items/{item_name}")
def Find(item_name: str):
    for i in all_items:
        if i.name == item_name:
            return i
    return {'error': 'Item not found!'}

@app.post("/items/")
def Upload(item: Item):
    all_items.append(item)
    return item

@app.put("/items/{item_name}")
def Update(item_name: str, item: Item):
    for i in all_items:
        if i.name == item_name:
            i.name = item.name
            i.description = item.description
            i.price = item.price
            return i
    return {'error': 'Item not found!'}

@app.delete("/items/{item_name}")
def Delete(item_name: str):
    for i in all_items:
        if i.name == item_name:
            all_items.remove(i)
            return {'message': 'item deleted'}
    return {'error': 'Item not found!'}
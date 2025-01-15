from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI()

# MongoDB connection and setup
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://root:example@mongodb:27017/Store?authSource=admin")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["Store"]
collection = db["Items"]

# Pydantic model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

# Helper function to convert MongoDB ObjectId to string
def item_helper(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"]
    }

# Routes

@app.get("/items/{item_name}", response_model=Item)
async def find_item(item_name: str):
    item = await collection.find_one({"name": item_name})
    if item:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/", response_model=Item)
async def upload_item(item: Item):
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    item_dict["_id"] = str(result.inserted_id)
    return item_dict

@app.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str, item: Item):
    existing_item = await collection.find_one({"name": item_name})
    if existing_item:
        updated_item = await collection.find_one_and_update(
            {"name": item_name},
            {"$set": item.dict()},
            return_document=True
        )
        return item_helper(updated_item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_name}", response_model=dict)
async def delete_item(item_name: str):
    result = await collection.delete_one({"name": item_name})
    if result.deleted_count == 1:
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.on_event("startup")
async def startup_db_client():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

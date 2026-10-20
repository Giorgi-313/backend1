from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Python API", version="1.0.0")


class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)


class ItemResponse(Item):
    id: int


items_db: dict[int, ItemResponse] = {
    1: ItemResponse(id=1, name="Laptop", price=999.99),
    2: ItemResponse(id=2, name="Mouse", price=25.50),
}

@app.get("/")
def home():
    return {"message": "Welcome to the Python API - Pipeline Fully Automated!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def get_items():
    return list(items_db.values())


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = items_db.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@app.post("/items", status_code=201)
def create_item(item: Item):
    new_id = max(items_db.keys(), default=0) + 1

    created_item = ItemResponse(
        id=new_id,
        name=item.name,
        price=item.price,
    )

    items_db[new_id] = created_item
    return created_item
from fastapi import FastAPI, HTTPException from pydantic import BaseModel, Field

app = FastAPI(title="Python API", version="1.0.0")

class Item(BaseModel): name: str = Field(min_length=1) price: float = Field(gt=0)

class ItemResponse(Item): id: int

items_db: dict[int, ItemResponse] = { 1: ItemResponse(id=1, name="Laptop", price=999.99), 2: ItemResponse(id=2, name="Mouse", price=25.50), }

@app.get("/") def home(): return {"message": "Welcome to the Python API"}

@app.get("/health") def health(): return {"status": "ok"}

@app.get("/items") def getitems(): return list(itemsdb.values())

@app.get("/items/{itemid}") def getitem(itemid: int): item = itemsdb.get(item_id)

if item is None: raise HTTPException(status_code=404, detail="Item not found")

	return item

@app.post("/items", statuscode=201) def createitem(item: Item): newid = max(itemsdb.keys(), default=0) + 1

	createditem = ItemResponse( id=newid, name=item.name, price=item.price, )

itemsdb[newid] = createditem return createditem
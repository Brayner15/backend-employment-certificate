from fastapi import FastAPI
app = FastAPI()
# from app.routers import items
from app.routers.create_pdf_analytics import router

# app.include_router(items.router, prefix="/items", tags=["items"])
# app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(router)

@app.get("/", tags=['Home'])
async def get_status():
    return {}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from booklinker import search_books, save_links_to_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    maxPages: int = 5

class SaveLinksRequest(BaseModel):
    links: List[str]

@app.post("/api/search")
async def search(request: SearchRequest):
    books = search_books(request.query, request.maxPages)
    return {"books": books}

@app.post("/api/save-links")
async def save_links(request: SaveLinksRequest):
    save_links_to_file(request.links)
    return {"status": "success", "message": f"Saved {len(request.links)} links"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

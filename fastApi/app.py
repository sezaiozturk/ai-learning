from sentence_transformers import SentenceTransformer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import chromadb 
import ollama
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chroma_client = chromadb.PersistentClient(path = "chroma_db")
collection = chroma_client.get_or_create_collection(name = "texts")

def getEmbedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]



@app.get("/")
def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/addText")
async def addText(request: Request):
    data = await request.json()
    embedding = getEmbedding(data["text"])
    id = str(uuid.uuid4())
    collection.add(ids=[id], embeddings=[embedding], metadatas=[{"text": data["text"]}])
    return JSONResponse(content=data)

@app.post("/searchText")
async def searchText(request: Request):
    data = await request.json()
    query_embedding = getEmbedding(data["text"])
    results = collection.query(query_embeddings = [query_embedding], n_results = 5)
    return results["metadatas"]

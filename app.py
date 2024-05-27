from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mixedbread import MixBreadEmbeddings
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
import os

MODEL = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL
    MODEL = MixBreadEmbeddings('mixedbread-ai/mxbai-embed-large-v1')
    yield

class UserQuery(BaseModel):
    text: str

class DocumentsInput(BaseModel):
    texts: List[str]

class EmbeddingsQueryOutput(BaseModel):
    embeddings: List[float]

class EmbeddingsDocumentOutput(BaseModel):
    embeddings: List[List[float]]


# FastAPI Initialization
app = FastAPI(
    title="Backend for MixedBread Embeddings",
    lifespan=lifespan, 
    docs_url="/", 
    root_path=os.getenv("TFY_SERVICE_ROOT_PATH")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def status():
    return JSONResponse(content={"status": "OK"})


# openapi example:
QUERY_EXAMPLE = {
    "example-request" : {
        "summary": "Example request for embedding the query",
        "value": UserQuery(text="Hello, World!")
    }
}

@app.post("/embed-query")
async def embed_query(query: UserQuery = Body(..., openapi_examples=QUERY_EXAMPLE)) -> EmbeddingsQueryOutput:
    assert MODEL is not None
    response = await MODEL.embed_query(query.text)
    return EmbeddingsQueryOutput(embeddings=response)


# openapi example:
DOCUMENT_QUERY_EXAMPLE = {
    "example-request" : {
        "summary": "Example request for embedding the documents",
        "value": DocumentsInput(texts=["Hello, World!", "Good morning!"])
    }
}

@app.post("/embed-documents")
async def embed_documents(documents: DocumentsInput = Body(..., openapi_examples=DOCUMENT_QUERY_EXAMPLE)) -> EmbeddingsDocumentOutput:
    assert MODEL is not None
    response = await MODEL.embed_documents(documents.texts)
    return EmbeddingsDocumentOutput(embeddings=response)


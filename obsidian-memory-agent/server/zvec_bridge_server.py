import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import zvec
import os

app = FastAPI(title="Zvec Bridge Server")

# Global collection reference
collection = None
COLLECTION_PATH = "./zvec_db"

class InitRequest(BaseModel):
    collection_name: str
    dimension: int
    db_path: Optional[str] = None

class VectorData(BaseModel):
    embedding: List[float]

class DocItem(BaseModel):
    id: str
    vectors: Dict[str, List[float]]
    fields: Dict[str, Any]

class QueryRequest(BaseModel):
    vector: List[float]
    top_k: int = 5
    vector_field: str = "embedding"

@app.get("/health")
def health_check():
    return {"status": "ok", "zvec_version": "0.1.0"} # Assuming version

@app.post("/init")
def init_collection(req: InitRequest):
    global collection
    try:
        path = req.db_path if req.db_path else COLLECTION_PATH
        # Ensure directory exists
        os.makedirs(path, exist_ok=True)
        
        schema = zvec.CollectionSchema(
            name=req.collection_name,
            vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, req.dimension),
        )
        collection = zvec.create_and_open(path=path, schema=schema)
        return {"status": "initialized", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/insert")
def insert_docs(docs: List[DocItem]):
    global collection
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not initialized")
    
    try:
        zvec_docs = []
        for d in docs:
            zvec_docs.append(zvec.Doc(id=d.id, vectors=d.vectors, fields=d.fields))
        
        collection.insert(zvec_docs)
        return {"status": "inserted", "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_docs(req: QueryRequest):
    global collection
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not initialized")
    
    try:
        matches = collection.query(
            zvec.VectorQuery(req.vector_field, vector=req.vector),
            topk=req.top_k
        )
        
        results = []
        for match in matches:
            results.append({
                "id": match.id,
                "score": match.score,
                "fields": match.fields
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Zvec Bridge Server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

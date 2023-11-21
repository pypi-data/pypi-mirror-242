from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from storage import Database
connection_string = "postgresql://root:WOxqVe0lK+6XZY66FkuNRg==@34.30.181.130:5432/demo_sa"
db = Database(connection_string)

app = FastAPI()

class DatabaseCreateBody(BaseModel):
    name: str
    vector_length: int = 2
    max_vectors: int = 10_000

@app.post("/database/create")
def databaseCreate(body: DatabaseCreateBody):
    db.create_table(body.name, vector_length=body.vector_length, max_vectors=body.max_vectors)
    return {"message": "Success"}

@app.get("/database/list-tables")
def databaseListTables():
    return db.list_tables()

class TableAddBody(BaseModel):
    table_name: str
    embedding: str

@app.post("/table/add")
def tableAdd(body: TableAddBody):
    table = db.load(body.table_name)
    table.add(eval(body.embedding))
    return {"message": "Success"}

class TableBatchAddBody(BaseModel):
    table_name: str
    embeddings: list

@app.post("/table/batch-add")
def tableBatchAdd(body: TableBatchAddBody):
    table = db.load(body.table_name)
    # convert each string in the list to a tuple
    body.embeddings = [eval(embedding) for embedding in body.embeddings]
    table.batch_add(body.embeddings)
    return {"message": "Success"}

@app.get("/table/semantic-query")
def tableSemanticQuery(table_name: str, embedding_vector: str, num_results: int, pf_blocks: int = None, pf_thresh: float = None, metadata_filter: dict = None):
    table = db.load(table_name)
    return table.semantic_query(embedding_vector, num_results, pf_blocks, pf_thresh, metadata_filter)

@app.get("/table/keyword-query")
def tableKeywordQuery(table_name: str, keyword: str, num_results: int, metadata_filter: dict = None):
    table = db.load(table_name)
    return table.keyword_query(keyword, num_results, metadata_filter)

@app.get("/table/hybrid-query")
def tableHybridQuery(table_name: str, keyword: str, embedding_vector: str, num_results: int, metadata_filter: dict = None):
    table = db.load(table_name)
    return table.hybrid_query(keyword, embedding_vector, num_results, metadata_filter)

@app.delete("/table/delete")
def tableDelete(table_name: str):
    table = db.load(table_name)
    table.delete()
    return {"message": "Success"}

class TableClearBody(BaseModel):
    table_name: str

@app.post("/table/clear")
def tableClear(body: TableClearBody):
    table = db.load(body.table_name)
    table.clear()
    return {"message": "Success"}
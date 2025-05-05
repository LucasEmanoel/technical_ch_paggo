from typing import List
from fastapi import FastAPI, Query

from helper import ManagerDB
from services import DataService

app = FastAPI()

@app.get("/")
async def root():
  connector = ManagerDB()
  connector.create_db()
  connector.seed()
  return {"db": "Banco criado + valores inseridos"}

@app.get("/listar")
async def get_data(start: str = None, end: str = None, variables: List[str] = Query([])):
  #print(variables)
  
  service = DataService()
  result = service.listByDate(start, end, variables)
  
  return result

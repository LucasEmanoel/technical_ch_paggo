from datetime import datetime
from typing import Optional
from fastapi import FastAPI

from helper import ManagerDB
from services import DataService


connector = ManagerDB()
connector.create_db()
connector.seed()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/listar")
async def get_data(start: str = None, end: str = None):
  start = datetime.strftime(start, '%d/%m/%Y')
  end = datetime.strftime(end, '%d/%m/%Y')
    
  service = DataService()
  result = service.listByDate(start, end)
  
  return result

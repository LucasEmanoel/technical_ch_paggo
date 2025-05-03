from datetime import datetime, timedelta

from fastapi import HTTPException
from model import Data
from helper import ManagerDB
from sqlalchemy.orm import Session

class DataService:
  
  def __init__(self):
    self.manager = ManagerDB()
    
  def listByDate(self, start: datetime, end: datetime):

    
    if start > end:
      raise HTTPException(status_code=400, detail="data final deve ser maior que inicial")
    
    with Session(self.manager.engine()) as session:
      result = ( 
        session.query(Data)
        .filter(Data.timestamp <= end) #consulta
        .filter(Data.timestamp >= start)
        .all()
      )

    return result

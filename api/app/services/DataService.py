from datetime import datetime, time
from typing import List

from fastapi import HTTPException
from model import Data
from helper import ManagerDB
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only

class DataService:
  
  def __init__(self):
    self.manager = ManagerDB()
    
  def listByDate(self, start: str, end: str, variables: List[str]):
    
    if not 'timestamp' in variables:
      variables.append('timestamp')
      
    new_start = datetime.strptime(start, '%d/%m/%Y')
    new_start = datetime.combine(new_start, time.min)
    new_end = datetime.strptime(end, '%d/%m/%Y')
    new_end = datetime.combine(new_end, time.max)
      
    if new_start > new_end:
      raise HTTPException(status_code=400, detail="data final deve ser maior que inicial")
    
    with Session(self.manager.engine()) as session:
      
      result = (
        session.query(Data)
          .filter(Data.timestamp >= new_start)
          .filter(Data.timestamp <= new_end)
          .all()
      )

    filterd_result = [ { var : getattr(item, var) for var in variables } for item in result ]
    return filterd_result

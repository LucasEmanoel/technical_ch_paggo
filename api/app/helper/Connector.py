import os

from data import seed
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class ManagerDB:
  
  def __init__(self):
    load_dotenv()
    self.db_url = os.getenv('DB_CONNECTION')
    self._engine = None
    
  def connection(self) -> Engine:
    if not self._engine:
      self._engine = create_engine(self.db_url)
      
    return self._engine
  
  def seed(self):
    return seed.generate_rows()
    
    
  
  


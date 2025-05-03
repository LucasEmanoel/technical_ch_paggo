import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from model import Base


class ManagerDB:
  def __init__(self):
    load_dotenv(override=True)
    url = os.environ.get('DB_DESTINATION_URL')
    self._engine = create_engine(url)
    
  def create_db(self):
    Base.metadata.create_all(self._engine)
    
    
  
  


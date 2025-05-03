import os

from datetime import datetime, timedelta, timezone
import random

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from model import Base, Data


class ManagerDB:
  def __init__(self):
    load_dotenv()
    self._engine = create_engine(os.environ.get('DB_SOURCE_URL'))
    
  def create_db(self):
    Base.metadata.create_all(self._engine)
    
  def engine(self):
    return self._engine
  
  def seed(self):
    init = datetime.now(timezone.utc)
    period = 10 * 24 * 60 

    data = [
      Data(
        timestamp = init - timedelta(minutes=i),
        wind_speed = random.uniform(0, 30),
        power = random.uniform(0, 100),
        ambient_temprature = random.uniform(-20, 40)
      )
      for i in range(period)
    ]
    
    with Session(self._engine) as session:
      session.add_all(data)
      session.commit()
    
    
  
  


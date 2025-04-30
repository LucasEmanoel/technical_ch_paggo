from datetime import datetime, timedelta, timezone
import random

def generate_rows():
  init = datetime.now(timezone.utc)
  insert_block = []
  period = 10 * 24 * 60 

  insert_block = [
    {
      'timestamp': init + timedelta(minutes=i),
      'wind_speed': random.uniform(0, 30),
      'power': random.uniform(0, 100),
      'ambient_temprature': random.uniform(-20, 40)
    }
    for i in range(period)
  ]
  
  return insert_block


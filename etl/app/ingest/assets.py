from datetime import datetime
import json
from typing import List
import httpx
import pandas as pd
from pandas import DataFrame
import dagster as dg
from requests import Session
from sqlalchemy import create_engine
from dagster import Any, DailyPartitionsDefinition, Definitions, Dict, define_asset_job
from sqlalchemy.orm import sessionmaker

from model import Signal, SignalType

# class DataResourceDB(dg.ConfigurableResource):
#     url_source_db: str

#     @property
#     def query_string(self) -> str:
#         return self.url_source_db

#     def get_connection(self):
#       return create_engine(self.url_source_db).connect()
      
class DataResourceApi(dg.ConfigurableResource):
    
    url: str
    
    @property
    def query_string(self) -> str:
        return self.url
    
    def get_data(self, params) -> str:
        result = httpx.get(self.query_string, params=params)
        data = result.json()
        return data
      
class SignalResourceDB(dg.ConfigurableResource):
    url_destination_db: str

    @property
    def engine(self):
        return create_engine(self.url_destination_db)

class SetupResource(dg.ConfigurableResource):
    variables: List[str]
    period: str
    operations: List[str]
    
    
    
#### ASSETS ####

daily_partition = DailyPartitionsDefinition(
    start_date="2025-05-02", timezone="America/Recife"
)

@dg.asset(partitions_def=daily_partition)
def extract_from_source_db(context, data_resource_api: DataResourceApi) -> DataFrame:

  date = context.partition_key
  date_obj = datetime.strptime(date, "%Y-%m-%d")
  formatted_date = date_obj.strftime("%d/%m/%Y")
  
  variables = ['wind_speed','power']

  params = { 
            'start'      : formatted_date,
            'end'        : formatted_date,
            'variables'  : variables
            }

  result = data_resource_api.get_data(params)
  return pd.DataFrame(result)
  
@dg.asset(partitions_def=daily_partition)
def transform_data(context, extract_from_source_db: DataFrame, signal_resource_db: SignalResourceDB):
    
  period = '10Min'
  agg_rows = 10
  operations = ['mean', 'min', 'max', 'std']
  variables = ['wind_speed','power']
  
  df = extract_from_source_db
  df['timestamp'] = pd.to_datetime(df['timestamp'])
  df.set_index('timestamp', drop=True, inplace=True)
  
  agg_data = [{var: i for var in variables } for i in operations]
  
  results = []
  for item in agg_data:
    for key, val in item.items():
        new_df = df.resample(period).agg(item)
        new_df['op'] = val

        results.append(new_df)

  final_r = pd.concat(results)
    
    

  
  Session = sessionmaker(signal_resource_db.engine)
  
  with Session() as session:
    signal_types = session.query(SignalType).all()
    signal_types_map = {(s.signal_operation, s.signal_type, s.agg_rows) : s.id for s in signal_types}
    
    final_r.reset_index(inplace=True)
  
    pivoted = final_r.melt(
      id_vars=['timestamp', 'op'],  
      value_vars=['wind_speed', 'power'],
      var_name='signal_type',
      value_name='value'
    )
    
    insert_list = pivoted.to_dict(orient='records')
  
    signals = []
    for signal in insert_list:
        key = (signal['op'], signal['signal_type'], agg_rows)
        if key in signal_types_map:
            signals.append(
                Signal(
                timestamp = signal['timestamp'],
                value = signal['value'],
                signal_id = signal_types_map[key]
                )
            )
    session.add_all(signals)
    session.commit()


daily_signal_job = dg.define_asset_job(
    name="daily_signal_job",
    selection=[extract_from_source_db, transform_data],
)

@dg.schedule(
    job=daily_signal_job,
    cron_schedule="0 1 * * *", 
)
def daily_exec(context):
    previous_day = context.scheduled_execution_time.date() - datetime.timedelta(days=1)
    date = previous_day.strftime("%Y-%m-%d")
    return dg.RunRequest(
        run_key=date,
        partition_key=date,
    )


defs = dg.Definitions(
    assets=[extract_from_source_db, transform_data],
    jobs=[define_asset_job('daily_signal_job')],
    resources={ 
        "data_resource_api": DataResourceApi(
            url='http://localhost:8000/listar'
        ),
        "signal_resource_db": SignalResourceDB(
            url_destination_db='postgresql+psycopg://postgres:admin@localhost:5432/destination_db'
        )
        
    }
)

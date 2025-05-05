import dagster as dg
import pandas as pd

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from pandas import DataFrame

from model import Base, Signal, SignalType
from etl_code.resources import DataResourceApi, SignalResourceDB, SetupResource


daily_partition = dg.DailyPartitionsDefinition(
    start_date="2025-04-25", timezone="America/Recife"
)

@dg.op
def initialize_destination_database(context, signal_resource_db: SignalResourceDB, setup: SetupResource):
    engine = signal_resource_db.engine
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(signal_resource_db.engine)
    
    with Session() as session:
        exists = session.query(SignalType).first()
        
        if exists:
            context.log.info('banco de dados já inicializado')
            return
        
        data = [
            SignalType(
            name = f'{i}_{j}_agg_{setup.get_period}',
            signal_type = i,
            signal_operation = j,
            agg_rows = setup.get_agg_rows
            )
            for i in setup.get_variables
            for j in setup.get_operations
        ]
        session.add_all(data)
        session.commit()   
        
        context.log.info('Tipos de sinais gerados no banco de dados')
        
@dg.asset(partitions_def=daily_partition)
def extract_from_source_db(context, data_resource_api: DataResourceApi, setup: SetupResource) -> DataFrame:

  start_dt = context.partition_time_window.start
  end_dt = context.partition_time_window.end

  formatted_start = start_dt.strftime("%d/%m/%Y")
  formatted_end = end_dt.strftime("%d/%m/%Y")
  

  params = { 
            'start'      : formatted_start,
            'end'        : formatted_end,
            'variables'  : setup.get_variables
            }

  result = data_resource_api.get_data(params)
  return pd.DataFrame(result)
  
@dg.asset(partitions_def=daily_partition)
def transform_data(context, extract_from_source_db, setup: SetupResource) -> list[dict]:

    df = extract_from_source_db
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', drop=True, inplace=True)
    
    agg_data = [{var: i for var in setup.get_variables } for i in setup.get_operations]
    
    results = []
    for item in agg_data:
        for key, val in item.items():
            new_df = df.resample(setup.get_period).agg(item)
            new_df['op'] = val

            results.append(new_df)

    final_r = pd.concat(results)
    final_r.reset_index(inplace=True)
  
    pivoted = final_r.melt(
      id_vars=['timestamp', 'op'],  
      value_vars=['wind_speed', 'power'],
      var_name='signal_type',
      value_name='value'
    )
    
    insert_list = pivoted.to_dict(orient='records')
    
    return insert_list
  

@dg.asset(partitions_def=daily_partition)
def load_data(context, transform_data, signal_resource_db: SignalResourceDB, setup: SetupResource):
    
    data = transform_data
    
    Session = sessionmaker(signal_resource_db.engine)
    with Session() as session:
        
        signal_types = session.query(SignalType).all()
        signal_types_map = {(s.signal_operation, s.signal_type, s.agg_rows) : s.id for s in signal_types}
        
        signals = []
        for signal in data:
            key = (signal['op'], signal['signal_type'], setup.get_agg_rows)
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





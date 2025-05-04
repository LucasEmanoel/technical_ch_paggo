import httpx
from model import SignalType, Signal
from helper import ManagerDB
import pandas as pd
from sqlalchemy.orm import Session

connector = ManagerDB()
connector.create_db()

# 1. recebe data
#data = input('Digite uma data válida! Ex:(02/05/2025):')
date = '02/05/2025'
variables = ['wind_speed','power']
period = '10Min'
agg_rows = 10
operations = ['mean', 'min', 'max', 'std']

# 2. consulta
params = { 
           'start'      : date,
           'end'        : date,
           'variables'  : variables
          }


result = httpx.get(f'http://localhost:8000/listar', params=params)

# 3. agrega a cada 10-minutal

data_csv = pd.DataFrame(result.json())
data_csv['timestamp'] = pd.to_datetime(data_csv['timestamp'])
data_csv.set_index('timestamp', drop=True, inplace=True)

agg_data = [{var: i for var in variables } for i in operations]

results = []
for item in agg_data:
  for key, val in item.items():
    new_df = data_csv.resample(period).agg(item)
    new_df['op'] = val

    results.append(new_df)

final_r = pd.concat(results)

# 4. Salvar no db

manager = ManagerDB()
# with Session(manager.engine()) as session:
#   signals_types = ['wind_speed', 'power']
#   signals_op = ['mean', 'min', 'max', 'std']
  
#   data = [
#     SignalType(
#       name = f'{i}_{j}_agg_{period}',
#       signal_type = i,
#       signal_operation = j,
#       agg_rows = agg_rows
#     )
#     for i in signals_types
#     for j in signals_op
#    ]
#   session.add_all(data)
#   session.commit()
  
with Session(manager.engine()) as session:
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

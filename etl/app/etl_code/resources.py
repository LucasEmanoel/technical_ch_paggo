from typing import List
import dagster as dg
import httpx
from sqlalchemy import create_engine

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
    agg_rows: int
    
    @property
    def get_variables(self):
        return self.variables
    
    @property
    def get_period(self):
        return self.period
    
    @property
    def get_operations(self):
        return self.operations
    
    @property
    def get_agg_rows(self):
        return self.agg_rows
    
    
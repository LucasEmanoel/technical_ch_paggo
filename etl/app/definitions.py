from datetime import datetime
import os
from dotenv import load_dotenv
import etl_code.assets
from etl_code.jobs import daily_signal_job, initialize_database_job, daily_schedule
from etl_code import DataResourceApi, SignalResourceDB, SetupResource
import dagster as dg


all_assets = dg.load_assets_from_modules([etl_code.assets])
    
defs = dg.Definitions(
    assets=all_assets,
    jobs=[initialize_database_job, daily_signal_job],
    schedules=[daily_schedule],
    resources={ 
        "data_resource_api": DataResourceApi(
            url='http://api_service:80/listar'
        ),
        "signal_resource_db": SignalResourceDB(
            url_destination_db='postgresql+psycopg://postgres:admin@postgres_db_destination:5432/destination_db'
        ),
        "setup": SetupResource(
            variables=["wind_speed", "power"],
            period="10Min",
            operations=["mean", "min", "max", "std"],
            agg_rows=10
        )
    }
)

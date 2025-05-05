# etl_code/jobs.py
import dagster as dg
from .assets import initialize_destination_database



@dg.job
def initialize_database_job():
    initialize_destination_database()

daily_signal_job = dg.define_asset_job(
    name="daily_signal_job",
    selection=dg.AssetSelection.keys("extract_from_source_db", "transform_data", "load_data")
)
 
daily_schedule = dg.ScheduleDefinition(
    job=daily_signal_job,
    cron_schedule="0 0 * * *",
    execution_timezone="America/Recife",
)
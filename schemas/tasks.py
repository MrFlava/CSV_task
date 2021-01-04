from CSVproject_main.celery import app
from .service import generate_csv_data


@app.task
def csv_generator(schema_id, rows):
    generate_csv_data(schema_id, rows)

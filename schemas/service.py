import csv
import random
import datetime
from faker import Faker
from .models import Column


def generate_csv_data(schema):
    fake = Faker()
    columns = Column.objects.filter(schema_id=schema)
    column_rows = [{column.name: None for column in columns} for _ in range(10)]

    for column in columns:
        for i in range(0, len(column_rows)):
            if column.type == 'PHONE_NUMBER':
                column_rows[i].update({column.name: fake.phone_number()})
            if column.type == 'FULL_NAME':
                column_rows[i].update({column.name: fake.name()})
            if column.type == 'JOB':
                column_rows[i].update({column.name: fake.job()})
            if column.type == 'EMAIL':
                column_rows[i].update({column.name: fake.email()})
            if column.type == 'COMPANY_NAME':
                column_rows[i].update({column.name: fake.company()})
            if column.type == 'TEXT':
                column_rows[i].update({column.name: fake.text()})
            if column.type == 'INTEGER':
                column_rows[i].update({column.name: random.randrange(column.from_range, column.to_range)})
            if column.type == 'ADDRESS':
                column_rows[i].update({column.name: fake.address()})
            if column.type == 'DATE':
                column_rows[i].update({column.name: fake.date()})
    csv_file = "CSVproject_main/media/data.csv"

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[column.name for column in columns])
            writer.writeheader()
            for data in column_rows:
                writer.writerow(data)
    except IOError:
        print("I/O error")

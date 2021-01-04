import csv
import random
import datetime
from faker import Faker
from .models import Column


def generate_csv_data(schema):
    fake = Faker()
    columns = Column.objects.filter(schema_id=schema)
    column_rows = [{column.name: None for column in columns} for _ in range(10)]
    row_types_methods = {'PHONE_NUMBER': 'fake.phone_number()', 'FULL_NAME': 'fake.name()', 'JOB': 'fake.job()',
                         'EMAIL': 'fake.email()', 'COMPANY_NAME': 'fake.company()', 'TEXT': 'fake.text()',
                         'INTEGER': 'random.randrange(column.from_range, column.to_range)', 'ADDRESS': 'fake.address()',
                         'DATE': 'fake.date()'}
    for column in columns:
        for i in range(0, len(column_rows)):
            if column.type in row_types_methods:
                column_rows[i].update({column.name: eval(row_types_methods[column.type])})

    csv_file = "CSVproject_main/media/data.csv"

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[column.name for column in columns])
            writer.writeheader()
            for data in column_rows:
                writer.writerow(data)
    except IOError:
        print("I/O error")

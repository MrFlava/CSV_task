import os
import csv
import random
import datetime
from faker import Faker

from .models import Column, Schema
from CSVproject_main.storage_backends import MediaStorage


def generate_csv_data(schema, rows):
    fake = Faker()
    media_storage = MediaStorage()
    columns = Column.objects.filter(schema_id=schema)
    schema = Schema.objects.get(pk=schema)
    column_rows = [{column.name: None for column in columns} for _ in range(rows)]
    column_names = []
    row_types_methods = {
        "PHONE_NUMBER": "fake.phone_number()",
        "FULL_NAME": "fake.name()",
        "JOB": "fake.job()",
        "EMAIL": "fake.email()",
        "COMPANY_NAME": "fake.company()",
        "DOMAIN_NAME": "fake.domain_name()",
        "TEXT": "fake.text()",
        "INTEGER": "random.randrange(column.from_range, column.to_range)",
        "ADDRESS": "fake.address()",
        "DATE": "fake.date()",
    }
    column_separators = {"TAB": "  ", "SEMICOLON": ";", "COMMA": ",", "SPACE": " "}
    string_characters = {"DOUBLE_QUOTE": '"', "COLONEL": "'"}
    for column in columns:
        column_names.insert(column.order, column.name)
        for i in range(0, len(column_rows)):
            column_rows[i].update({column.name: eval(row_types_methods[column.type])})

    try:
        i = 0
        while media_storage.exists(f"{schema.name}_{i}.csv"):
            i += 1

        with media_storage.open(f"{schema.name}_{i}.csv", "w") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                quoting=csv.QUOTE_ALL,
                fieldnames=column_names,
                delimiter=f"{column_separators[schema.column_separator]}",
                quotechar=string_characters[schema.string_character],
                escapechar="\\",
            )
            writer.writeheader()

            for data in column_rows:
                for key in data.keys():
                    data[key] = str(data[key]).replace(
                        " ", f"{column_separators[schema.column_separator]}"
                    )
                    if string_characters[schema.string_character] is '"':
                        data[key] = f'"{data[key]}"'
                    else:
                        data[key] = f"'{data[key]}'"

                writer.writerow(data)
    except IOError:
        print("I/O error")

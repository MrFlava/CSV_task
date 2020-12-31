import csv
import random
import datetime
from faker import Faker
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .models import Schema, Column, DataType
from .forms import SchemaForm, ColumnForm

# Create your views here.


def DashboardView(request):

    schemas = Schema.objects.all()

    context = {

        'schemas': schemas
    }
    return render(request=request, template_name="schemas/dashboard.html", context=context)


def NewSchemaView(request):

    if request.method == "POST":

        form = SchemaForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    else:
        form = SchemaForm()

    context = {'form': form}

    return render(request=request, template_name="schemas/schema.html", context=context)


# def DeleteColumnView(request):

def DeleteSchemaView(request, schema_id):

    try:
        schema = Schema.objects.get(pk=schema_id)

    except Schema.DoesNotExist:

        return HttpResponseRedirect("/")

    schema.delete()
    return HttpResponseRedirect("/")


def UpdateSchemaView(request, schema_id):

    schema = Schema.objects.get(pk=schema_id)
    schema.last_modified = datetime.datetime.now()

    form = SchemaForm(request.POST or None, instance=schema)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")

    context = {'form': form}

    return render(request=request, template_name="schemas/schema.html", context=context)


def ColumnsDashboardView(request, schema_id):

    columns = Column.objects.filter(schema_id=schema_id)

    context = {
        'schema_id': schema_id,
        'columns': columns
    }

    return render(request=request, template_name="schemas/dashboard.html", context=context)


def NewColumnView(request, schema_id):

    if request.method == "POST":

        column = Column.objects.create(schema_id=schema_id)

        form = ColumnForm(request.POST, instance=column)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    else:
        form = ColumnForm()

    context = {
        'form': form
    }

    return render(request=request, template_name="schemas/column.html", context=context)


# def DeleteColumnView(request):

def DeleteColumnView(request, column_id, schema_id):

    try:
        column = Column.objects.get(pk=column_id)

    except Column.DoesNotExist:

        return HttpResponseRedirect("/")

    column.delete()
    return HttpResponseRedirect("/")


def UpdateColumnView(request, column_id, schema_id):

    column = Column.objects.get(pk=column_id)

    form = ColumnForm(request.POST or None, instance=column)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")

    context = {'form': form}

    return render(request=request, template_name="schemas/column.html", context=context)


def GenerateDataView(request, schema_id):

    fake = Faker()
    columns = Column.objects.filter(schema_id=schema_id)
    column_rows = []

    for column in columns:
        for i in range(10):
            if column.type == 'PHONE_NUMBER':
                column_rows.append({column.name: fake.phone_number()})
            if column.type == 'FULL_NAME':
                column_rows.append({column.name: fake.name()})
            if column.type == 'JOB':
                column_rows.append({column.name: fake.job()})
            if column.type == 'EMAIL':
                column_rows.append({column.name: fake.email()})
            if column.type == 'COMPANY_NAME':
                column_rows.append({column.name: fake.company()})
            if column.type == 'TEXT':
                column_rows.append({column.name: fake.text()})
            if column.type == 'INTEGER':
                column_rows.append({column.name: random.randrange(column.from_range, column.to_range)})
            if column.type == 'ADDRESS':
                column_rows.append({column.name: fake.address()})
            if column.type == 'DATE':
                column_rows.append({column.name: fake.date()})
    context = {}

    csv_file = "CSVproject_main/media/data.csv"

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[column.name for column in columns])
            writer.writeheader()
            for data in column_rows:
                writer.writerow(data)

    except IOError:
        print("I/O error")

    # return render(request=request, template_name="schemas/column.html", context=context)

    return HttpResponse(content=context)

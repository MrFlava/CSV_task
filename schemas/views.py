import csv
import random
import datetime
from faker import Faker
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .models import Schema, Column, DataType
from .forms import SchemaForm, ColumnForm
from .tasks import csv_generator

# Create your views here.


def DashboardView(request):
    if request.user.is_authenticated:

        schemas = Schema.objects.all()

        context = {

            'schemas': schemas
        }
        return render(request=request, template_name="schemas/dashboard.html", context=context)

    else:
        return HttpResponseRedirect('login/')


def NewSchemaView(request):
    if request.user.is_authenticated:

        if request.method == "POST":

            form = SchemaForm(request.POST)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/")

        else:
            form = SchemaForm()

        context = {'form': form}

        return render(request=request, template_name="schemas/schema.html", context=context)

    else:
        return HttpResponseRedirect("login/")


def DeleteSchemaView(request, schema_id):
    if request.user.is_authenticated:

        try:
            schema = Schema.objects.get(pk=schema_id)

        except Schema.DoesNotExist:

            return HttpResponseRedirect("/")

        schema.delete()
        return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/login/")


def UpdateSchemaView(request, schema_id):
    if request.user.is_authenticated:

        schema = Schema.objects.get(pk=schema_id)
        schema.last_modified = datetime.datetime.now()

        form = SchemaForm(request.POST or None, instance=schema)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

        context = {'form': form}

        return render(request=request, template_name="schemas/schema.html", context=context)

    else:
        return HttpResponseRedirect("/login/")


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
    if request.user.is_authenticated:
        context = {}
        csv_generator.delay(schema_id)
        return HttpResponse(content=context)
    else:
        return HttpResponseRedirect("/login/")

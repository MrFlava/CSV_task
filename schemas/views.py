import datetime
from django.shortcuts import render, HttpResponseRedirect

from .models import Schema, Column
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

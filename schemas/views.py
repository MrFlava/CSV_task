import os
import csv
from faker import Faker
import datetime
import random
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.forms import inlineformset_factory

from .models import Schema, Column
from .forms import SchemaForm
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

        schema = Schema()
        schema_form = SchemaForm(instance=schema)
        ColumnInlineFormSet = inlineformset_factory(Schema, Column, fields=("name",  "type", "order",
                                                                            "from_range", "to_range"), extra=1)
        formset = ColumnInlineFormSet(instance=schema)

        if request.method == "POST":
            schema_form = SchemaForm(request.POST)

            formset = ColumnInlineFormSet(request.POST, request.FILES)

            if schema_form.is_valid():
                created_schema = schema_form.save(commit=False)
                formset = ColumnInlineFormSet(request.POST, request.FILES, instance=created_schema)

                if formset.is_valid():
                    created_schema.save()
                    formset.save()
                    # return HttpResponseRedirect(created_schema.get_absolute_url())
                    return HttpResponseRedirect("/")

        context = {
             "schema_form": schema_form,
             "formset": formset,
        }
        print(formset)

        return render(request=request, template_name="schemas/schema.html", context=context)

    else:
        return HttpResponseRedirect("login/")


def UpdateSchemaView(request, schema_id):
    if request.user.is_authenticated:
        schema = Schema.objects.get(pk=schema_id)
        schema_form = SchemaForm(instance=schema)
        ColumnInlineFormSet = inlineformset_factory(Schema, Column, fields=("name", "type", "order",
                                                                            "from_range", "to_range"), extra=1)
        formset = ColumnInlineFormSet(instance=schema)

        if request.method == "POST":
            schema_form = SchemaForm(request.POST, instance=schema)

            formset = ColumnInlineFormSet(request.POST, request.FILES)

            if schema_form.is_valid():
                created_schema = schema_form.save(commit=False)
                formset = ColumnInlineFormSet(request.POST, request.FILES, instance=created_schema)

                if formset.is_valid():
                    created_schema.save()
                    formset.save()
                    # return HttpResponseRedirect(created_schema.get_absolute_url())
                    return HttpResponseRedirect("/")

        context = {
             "schema_form": schema_form,
             "formset": formset,
        }
        print(formset)

        return render(request=request, template_name="schemas/schema.html", context=context)

    else:
        return HttpResponseRedirect("/login/")


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


def GenerateDataView(request, schema_id, rows):
    if request.user.is_authenticated:

        context = {}
        csv_generator.delay(schema_id, rows)
        return render(request=request, template_name="schemas/generated_data.html", context=context)
    else:
        return HttpResponseRedirect("/login/")


def download_csv(request):
    print('Download .csv...')
    # Full path of file
    file_path = 'CSVproject_main/media/data.csv'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="file/force_download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response



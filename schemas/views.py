import os
import time
import boto3
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

from .models import Schema, Column, DataType, ColumnSeparatorType, StringCharacterType
from .forms import SchemaForm
from .tasks import csv_generator
from CSVproject_main.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


# Create your views here.


@login_required
def dashboard_view(request):
    schemas = Schema.objects.all()

    context = {"schemas": schemas}
    return render(
        request=request, template_name="schemas/dashboard.html", context=context
    )


@login_required
def new_schema_view(request):
    schema = Schema()
    schema_form = SchemaForm(instance=schema)
    ColumnInlineFormSet = inlineformset_factory(
        Schema,
        Column,
        fields=("name", "type", "from_range", "to_range", "order"),
        extra=1,
    )
    formset = ColumnInlineFormSet(instance=schema)

    if request.method == "POST":
        schema_form = SchemaForm(request.POST)

        formset = ColumnInlineFormSet(request.POST, request.FILES)

        if schema_form.is_valid():
            created_schema = schema_form.save(commit=False)
            formset = ColumnInlineFormSet(
                request.POST, request.FILES, instance=created_schema
            )

            if formset.is_valid():
                created_schema.save()
                formset.save()
                return redirect(f"/schema/{created_schema.pk}/edit")
                # return HttpResponseRedirect(f"/schema/{created_schema.pk}/edit")

    context = {
        "schema_form": schema_form,
        "formset": formset,
        "data_type": DataType.choices(),
        "column_separator_types": ColumnSeparatorType.choices(),
        "string_character_types": StringCharacterType.choices(),
    }
    # print(context.get('formset'))
    return render(request=request, template_name="schemas/schema.html", context=context)


@login_required
def update_schema_view(request, schema_id):
    schema = Schema.objects.get(pk=schema_id)
    schema_form = SchemaForm(instance=schema)
    ColumnInlineFormSet = inlineformset_factory(
        Schema,
        Column,
        fields=("name", "type", "from_range", "to_range", "order"),
        extra=1,
    )
    formset = ColumnInlineFormSet(instance=schema)

    if request.method == "POST":
        schema_form = SchemaForm(request.POST, instance=schema)

        formset = ColumnInlineFormSet(request.POST, request.FILES)

        if schema_form.is_valid():
            created_schema = schema_form.save(commit=False)
            formset = ColumnInlineFormSet(
                request.POST, request.FILES, instance=created_schema
            )

            if formset.is_valid():
                created_schema.save()
                formset.save()
                return redirect(f"/schema/{created_schema.pk}/edit")

    context = {
        "schema_form": schema_form,
        "formset": formset,
        "data_types": DataType.choices(),
        "column_separator_types": ColumnSeparatorType.choices(),
        "string_character_types": StringCharacterType.choices(),
    }
    # print(context.get('formset'))
    return render(request=request, template_name="schemas/schema.html", context=context)


@login_required
def delete_schema_view(request, schema_id):
    try:
        schema = Schema.objects.get(pk=schema_id)

    except Schema.DoesNotExist:

        return HttpResponseRedirect("/")

    schema.delete()
    return HttpResponseRedirect("/")


@login_required
def data_sets_view(request, schema_id):
    schema = Schema.objects.get(pk=schema_id)
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    csv_files = []

    for csv_file in s3_client.list_objects(Bucket=AWS_STORAGE_BUCKET_NAME)['Contents']:

        if schema.name in csv_file['Key']:
            csv_files.append(
                {
                    "status": "ready",
                    "created": f"%s"
                               % csv_file['LastModified'],
                    "public_link": f'https://csv-task-bucket.s3.us-east-2.amazonaws.com/{csv_file["Key"]}'
                }
            )
    context = {"csv_files": enumerate(csv_files, start=1)}
    return render(
        request=request, template_name="schemas/data_sets.html", context=context
    )


@login_required
def generate_data_view(request, schema_id, rows):
    csv_generator.delay(schema_id, rows)
    return HttpResponseRedirect(f"/schema/{schema_id}/data_sets")


@login_required
def download_csv(request, csv_file):
    file_path = f"CSVproject_main/media/{csv_file}"
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="file/force_download")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response

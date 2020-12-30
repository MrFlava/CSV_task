import datetime
from django.shortcuts import render, HttpResponseRedirect

from .models import Schema
from .forms import SchemaForm

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

    return render(request=request, template_name="schemas/new_schema.html", context=context)


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

    return render(request=request, template_name="schemas/new_schema.html", context=context)

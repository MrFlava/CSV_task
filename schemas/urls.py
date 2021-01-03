"""CSVproject_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.DashboardView, name="schema-dashboard"),
    path('new_schema', views.NewSchemaView, name="new-schema"),
    path('schema/<int:schema_id>/edit', views.UpdateSchemaView, name="update-schema"),
    path('schema/<int:schema_id>/delete', views.DeleteSchemaView, name="delete-schema"),
    path('schema/<int:schema_id>/generate_data', views.GenerateDataView, name="generate-data"),
    path('schema/<int:schema_id>/columns/new_column', views.SchemaForm, name="new-column"),
    path('csv/download', views.download_csv, name='download_csv'),
]

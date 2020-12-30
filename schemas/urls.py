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
    path('schema/<int:schema_id>/columns', views.ColumnsDashboardView, name="columns-dashboard"),
    path('schema/<int:schema_id>/columns/new_column', views.NewColumnView, name="new-column"),
    path('schema/<int:schema_id>/columns/<int:column_id>/delete', views.DeleteColumnView, name="delete-column"),
    path('schema/<int:schema_id>/columns/<int:column_id>/edit', views.UpdateColumnView, name="edit-column"),

]

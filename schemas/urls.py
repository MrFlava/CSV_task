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
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_view, name="schema-dashboard"),
    path("new_schema", views.new_schema_view, name="new-schema"),
    path("schema/<int:schema_id>/edit", views.update_schema_view, name="update-schema"),
    path("schema/<int:schema_id>/delete", views.delete_schema_view, name="delete-schema"),
    path("schema/<int:schema_id>/data_sets", views.data_sets_view, name="data-sets"),
    path("schema/<int:schema_id>/data_sets/generate_data/rows/<int:rows>", views.generate_data_view, name="generate-data"),
    path("csv/download/<str:csv_file>", views.download_csv, name="download_csv"),
]

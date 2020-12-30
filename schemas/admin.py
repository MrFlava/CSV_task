from django.contrib import admin
from .models import Schema

# Register your models here.


class SchemaAdmin(admin.ModelAdmin):
    model = Schema


admin.site.register(Schema, SchemaAdmin)


from django.contrib import admin
from .models import Schema, Column

# Register your models here.


class SchemaAdmin(admin.ModelAdmin):
    model = Schema


class ColumnAdmin(admin.ModelAdmin):
    model = Schema


admin.site.register(Schema, SchemaAdmin)
admin.site.register(Column, ColumnAdmin)


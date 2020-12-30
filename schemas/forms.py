from django import forms

from .models import StringCharacterType, ColumnSeparatorType, Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "column_separator", "string_character"]
        labels = {'name': "Name", "column_separator": "Column separator", "string_character": "String character"}


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["name", "type", "order", "from_range", "to_range", "schema"]
        labels = {'name': "Name", "type": "Type", "order": "Order", "from_range": "From range", "to_range": "To range", "schema": "Schema"}

from django import forms

from .models import StringCharacterType, ColumnSeparatorType, Schema


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "column_separator", "string_character"]
        labels = {'name': "Name", "column_separator": "Column separator", "string_character": "String character"}

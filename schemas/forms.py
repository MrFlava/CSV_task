from django import forms

from .models import StringCharacterType, ColumnSeparatorType, Schema


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "column_separator", "string_character"]
        labels = {'name': "Name", "column_separator": "Column separator", "string_character": "String character"}


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "type", "order"]
        labels = {'name': "Name", "type": "Type", "order": "Order"}


class ColumnRangeForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "type", "order", "from_range", "to_range"]
        labels = {'name': "Name", "type": "Type", "order": "Order", "from_range": "From range", "to_range": "To range"}

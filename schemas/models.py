import enum
import datetime

from django.db import models

# Create your models here.


class ColumnSeparatorType(enum.Enum):

    TAB = 'Tab'
    SEMICOLON = 'Semicolon (;)'
    COMMA = 'Comma (,)'
    SPACE = 'Space'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class StringCharacterType(enum.Enum):

    DOUBLE_QUOTE = 'Double-quote (")'
    COLONEL = "Single-quote (')"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class DataType(enum.Enum):

    FULL_NAME = "Full name"
    JOB = "Job"
    EMAIL = "Email"
    PHONE_NUMBER = "Phone number"
    COMPANY_NAME = "Company name"
    DOMAIN_NAME = "Domain name"
    TEXT = "Text"
    INTEGER = "Integer"
    ADDRESS = "Address"
    DATE = "Date"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Schema(models.Model):

    name = models.CharField(max_length=120)
    column_separator = models.CharField(max_length=120, choices=ColumnSeparatorType.choices())
    string_character = models.CharField(max_length=120, choices=StringCharacterType.choices())
    last_modified = models.DateTimeField(default=datetime.datetime.now())

    objects = models.Manager()

    def __str__(self):
        return f"Schema #{self.pk}"


class Column(models.Model):

    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120, choices=DataType.choices())
    order = models.PositiveIntegerField(default=0)
    from_range = models.PositiveIntegerField(null=True, blank=True)
    to_range = models.PositiveIntegerField(null=True, blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f"Column #{self.pk}"

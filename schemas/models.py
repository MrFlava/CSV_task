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


class Schema(models.Model):

    name = models.CharField(max_length=120)
    column_separator = models.CharField(max_length=120, choices=ColumnSeparatorType.choices())
    string_character = models.CharField(max_length=120, choices=StringCharacterType.choices())

    objects = models.Manager()

    def __str__(self):
        return f"Schema #{self.pk}"

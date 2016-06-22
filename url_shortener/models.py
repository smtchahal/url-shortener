from django.db import models
from django.core.validators import RegexValidator


class Link(models.Model):
    url = models.URLField(max_length=2083)
    alias = models.CharField(max_length=255, unique=True, validators=[
        RegexValidator(
            regex=r'^[a-zA-Z0-9-_]+$',
            message='Alias can only contain alphabets, numerals, underscores and hyphens',
        ),
    ])

    def __str__(self):
        return '{0} -> {1}'.format(self.alias, self.url)

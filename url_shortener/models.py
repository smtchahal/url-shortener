from django.db import models
from django.core.validators import RegexValidator


class Link(models.Model):
    url = models.URLField(max_length=2083)
    alias = models.CharField(max_length=255, unique=True, validators=[
        RegexValidator(
            regex=r'^[a-z0-9-_]+$',
            code='invalid_alias',
            message='Alias can only contain lowercase alphabets, numerals, underscores and hyphens',
        ),
    ])
    clicks_count = models.PositiveIntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{0} -> {1}'.format(self.alias, self.url)

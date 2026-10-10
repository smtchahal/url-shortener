import secrets
import string

from hashids import Hashids
from django.urls import reverse

HASH_SALT = 'VyIZlWoq7VQCvJmq54gVHz5mb7GbaXdcT3Qz8dRssMyaYpTZl2ONBBnDA788Ef'
ALPHABET = string.ascii_lowercase
ALIAS_LENGTH = 7

hashids = Hashids(salt=HASH_SALT, alphabet=ALPHABET)


def hash_encode(num):
    """
    Returns hashids.encode(num) with salt.
    """
    return hashids.encode(num)


def generate_alias(length=ALIAS_LENGTH):
    """
    Returns an unused alias drawn from a CSPRNG, so the next alias
    can't be predicted from the database state.
    """
    from .models import Link

    while True:
        alias = ''.join(secrets.choice(ALPHABET) for _ in range(length))
        if not Link.objects.filter(alias__iexact=alias).exists():
            return alias


def get_absolute_short_url(request, alias, remove_schema=True):
    """
    Returns absolute redirect URL, given the `request` object
    and the `alias`.

    Set `remove_schema` to False to prevent schema
    from being removed (default: True).
    """
    if alias:
        full_url = request.build_absolute_uri(
            reverse('url_shortener:alias', args=(alias,)))
    else:
        full_url = request.build_absolute_uri(reverse('url_shortener:index'))
    if remove_schema:
        return full_url[len(request.scheme)+3:]
    return full_url

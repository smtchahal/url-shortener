from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import (HttpResponseRedirect,
                         HttpResponsePermanentRedirect)

from .misc import (hash_encode,
                   get_absolute_short_url)
from .forms import URLShortenerForm
from .models import Link


def index(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            original_alias = form.cleaned_data['alias']
            alias = original_alias.lower()
            url = form.cleaned_data['url']
            new_link = Link(url=url)
            try:
                latest_link = Link.objects.latest('id')
                if Link.objects.filter(alias__exact=alias):
                    # handle alias conflict
                    new_link.alias = hash_encode(latest_link.id+1)
                    messages.add_message(request, messages.INFO,
                                         'Short URL {} already exists so a new short URL was created.'
                                         .format(get_absolute_short_url(request, original_alias)))
                    original_alias = new_link.alias
                else:
                    new_link.alias = alias or hash_encode(latest_link.id+1)
            except Link.DoesNotExist:
                new_link.alias = alias or hash_encode(1)
            new_link.save()
            return HttpResponseRedirect(reverse('url_shortener:preview', args=(original_alias or new_link.alias,)))
    else:
        form = URLShortenerForm()
    return render(request, 'url_shortener/index.html', {
        'form': form,
        'absolute_index_url': get_absolute_short_url(request, ''),
    })


def preview(request, alias):
    link = get_object_or_404(Link, alias__iexact=alias)
    return render(request, 'url_shortener/preview.html', {
        'alias': alias,
        'absolute_short_url': get_absolute_short_url(request, alias),
        'url': link.url,
    })


def redirect(request, alias):
    link = get_object_or_404(Link, alias__iexact=alias)
    return HttpResponsePermanentRedirect(link.url)

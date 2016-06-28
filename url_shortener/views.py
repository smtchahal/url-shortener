from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import (HttpResponseRedirect,
                         HttpResponsePermanentRedirect)

from .misc import hash_encode
from .forms import URLShortenerForm
from .models import Link


def index(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            alias = form.cleaned_data['alias']
            url = form.cleaned_data['url']
            new_link = Link(url=url)
            try:
                latest_link = Link.objects.latest('id')
                if Link.objects.filter(alias=alias):
                    new_link.alias = hash_encode(latest_link.id+1)
                else:
                    new_link.alias = alias or hash_encode(latest_link.id+1)
            except Link.DoesNotExist:
                new_link.alias = alias or hash_encode(1)
            new_link.save()
            return HttpResponseRedirect(reverse('url_shortener:redirect', kwargs={
                'alias': new_link.alias,
                'preview': '+',
            }))
    else:
        form = URLShortenerForm()
    return render(request, 'url_shortener/index.html', {'form': form})


def redirect(request, alias, preview=''):
    link = get_object_or_404(Link, alias=alias)
    if preview:
        abs_uri = request.build_absolute_uri()
        full_alias = abs_uri[len(request.scheme)+3:-1]  # scheme://[helloworld.com/alias]+
        return render(request, 'url_shortener/preview.html', {
            'alias': alias,
            'full_alias': full_alias,
            'url': link.url,
        })
    return HttpResponsePermanentRedirect(link.url)

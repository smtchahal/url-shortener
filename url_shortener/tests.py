from django.core.urlresolvers import reverse
from django.test import TestCase

from .misc import (id_to_alias,
                   alias_to_id)
from .forms import URLShortenerForm
from .models import Link

URL = 'https://www.example.com/'


class TestMiscFunctions(TestCase):

    def test_id_to_alias(self):
        self.assertEqual(id_to_alias(125), 'cb')
        self.assertEqual(id_to_alias(1), 'b')
        self.assertEqual(id_to_alias(578), 'ju')

    def test_alias_to_id(self):
        self.assertEqual(alias_to_id('cb'), 125)
        self.assertEqual(alias_to_id('b'), 1)
        self.assertEqual(alias_to_id('ju'), 578)


class TestRedirectView(TestCase):

    def test_redirect_with_invalid_alias(self):
        """
        URL with invalid alias should return 404.
        """
        response = self.client.get(reverse('url_shortener:redirect', kwargs={'alias': 'hkjlh'}))
        self.assertEqual(response.status_code, 404)

    def test_redirect_with_valid_alias(self):
        """
        URL with valid alias should redirect to appropriate URL
        with 301 response.
        """
        link = Link.objects.create(url=URL, alias='b')
        response = self.client.get(reverse('url_shortener:redirect', kwargs={'alias': 'b'}))
        self.assertRedirects(response, link.url, status_code=301)

    def test_redirect_preview_with_invalid_alias(self):
        """
        Preview URL with invalid alias should return 404 response.
        """
        response = self.client.get(reverse('url_shortener:redirect', kwargs={'alias': 'blah'}))
        self.assertEqual(response.status_code, 404)

    def test_redirect_preview_with_valid_alias(self):
        """
        Preview URL with valid alias should show a preview containing
        the URL to redirect to.
        """
        link = Link.objects.create(url=URL, alias='b')
        response = self.client.get(reverse('url_shortener:redirect', kwargs={'alias': 'b', 'preview': '+'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, link.url)


def create_link(url):
    """
    Helper function create a link.
    """
    link = Link.objects.create(url=url)
    link.alias = id_to_alias(link.id)
    link.save()
    return link


class TestIndexView(TestCase):

    def assert_link_created(self, response, alias):
        """
        Helper function to check whether a link was created successfully,
        given the `response` and the expected `alias`
        """
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('url_shortener:redirect', kwargs={
            'alias': alias,
            'preview': '+',
        }))
        self.assertTemplateUsed(response, 'url_shortener/preview.html')
        link = Link.objects.latest('id')
        self.assertEqual(link.url, URL)
        self.assertEqual(link.alias, alias)

    def test_index_with_no_alias_empty_database(self):
        """
        Submitting index form with no alias specified should
        create a link with auto-generated alias.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
        }, follow=True)
        self.assert_link_created(response, id_to_alias(1))

    def test_index_with_alias_empty_database(self):
        """
        Submitted index form with a specified alias should create
        a link with the specified alias.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': 'whatever',
        }, follow=True)
        self.assert_link_created(response, 'whatever')

    def test_index_with_no_alias_with_database(self):
        """
        Even if the database was pre-populated, submitting the form
        with no alias should create a new link as expected.
        """
        create_link(URL)
        latest_link = create_link(URL)
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
        }, follow=True)
        self.assert_link_created(response, id_to_alias(latest_link.id + 1))

    def test_index_with_alias_with_database(self):
        """
        Even if the database was pre-populated, submitting the form
        with a given alias should create a new link as expected.
        """
        create_link(URL)
        create_link(URL)
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': 'non-conflicting-alias',
        }, follow=True)
        self.assert_link_created(response, 'non-conflicting-alias')

    def test_index_with_conflicting_alias(self):
        """
        In case of a conflicting alias, auto-generated alias will be used
        and an appropriate message displayed.
        """
        link1 = create_link(URL)
        link2 = create_link(URL)
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': link1.alias,  # Uh oh, conflicts with the first link
        }, follow=True)
        self.assert_link_created(response, id_to_alias(link2.id + 1))

    def test_index_with_no_url_and_no_alias(self):
        """
        Index page when POSTed with no URL and no alias, should
        return an appropriate error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {}, follow=True)
        self.assertContains(response, 'Error')
        self.assertContains(response, 'field is required')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_no_url_and_valid_alias(self):
        """
        Index page when POSTed with no URL and a valid alias, should
        return an appropriate error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'alias': 'valid_alias',
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'field is required')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_no_url_and_invalid_alias(self):
        """
        Index page when POSTed with no URL and an invalid alias, should
        return an appropriate error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'alias': '/invalid/alias',
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'field is required')
        self.assertContains(response, 'hyphen')
        self.assertContains(response, 'underscore')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_invalid_alias(self):
        """
        Index page when POSTed invalid alias to, should return an appropriate
        error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': '/this/is/an/invalid/alias',
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'hyphen')
        self.assertContains(response, 'underscore')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_invalid_url(self):
        """
        Index page when POSTed invalid URL to, should return an appropriate
        error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': '/this/is/an/invalid/url',
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'Enter a valid URL')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_url_too_long(self):
        """
        Index page when POSTed a URL too long to should return an appropriate
        error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL + '?' + ''.join([str(c) for c in range(3000)]),
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'length')
        self.assertContains(response, '2083')
        self.assertTemplateUsed('url_shortener/index.html')

    def test_index_with_alias_too_long(self):
        """
        Index page when POSTed an alias too long to should return an appropriate
        error message.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': ''.join([id_to_alias(i) for i in range(300)]),
        })
        self.assertContains(response, 'Error')
        self.assertContains(response, 'length')
        self.assertContains(response, '255')
        self.assertTemplateUsed('url_shortener/index.html')


class TestURLShortenerFormValidation(TestCase):
    """
    Test form validation of URLShortenerForm. Not testing URL validation
    because URL validation is done by Django.
    """

    def test_alias_validation(self):

        VALID_ALIASES = ('there-you-go', 'this_is_okay', '42', '63as', 'alex42thegreat', 'R2-D2', 'E_D12')
        INVALID_ALIASES = ('stop$', '@asd', '#jgkl', '+hbwler', 'learn&grow', 'easy_peasy/', '/bye', ':huh', '(nope)',
                           '^acute', 'perc%tile', 'a*terisk', '<tag', 'you>', "'cause", '"possible"', '\\back', '=eq',
                           '|pipe', 'an{', 'fg}d', 'back`t', 'til~e', 'polls:index')

        for alias in VALID_ALIASES:
            form = URLShortenerForm(data={'url': URL, 'alias': alias})
            self.assertTrue(form.is_valid())

        for alias in INVALID_ALIASES:
            form = URLShortenerForm(data={'url': URL, 'alias': alias})
            self.assertTrue(not form.is_valid())

from django.core.urlresolvers import reverse
from django.test import TestCase

from .misc import hash_encode
from .forms import URLShortenerForm
from .models import Link

URL = 'https://www.example.com/'


class TestRedirectView(TestCase):

    def test_redirect_with_invalid_alias(self):
        """
        Redirect URL with invalid alias should return 404.
        """
        response = self.client.get(reverse('url_shortener:alias', args=('hkjlh',)))
        self.assertEqual(response.status_code, 404)

    def test_redirect_with_valid_alias(self):
        """
        Redirect URL with valid alias should redirect to appropriate URL
        with 301 response.
        """
        link = Link.objects.create(url=URL, alias='b')
        response = self.client.get(reverse('url_shortener:alias', args=('b',)))
        self.assertRedirects(response, link.url, status_code=301)
        link.refresh_from_db()
        self.assertEqual(link.clicks_count, 1)

    def test_redirect_with_uppercase_alias(self):
        """
        Redirect URL with various combinations of uppercase letters
        should always redirect to the same URL and refer to the same
        row in database.
        """
        link = Link.objects.create(url=URL, alias='some_alias')
        urls = (reverse('url_shortener:alias', args=('Some_Alias',)),
                reverse('url_shortener:alias', args=('some_alias',)),
                reverse('url_shortener:alias', args=('sOmE_aLIas',)))
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, URL, status_code=301)
        link.refresh_from_db()
        self.assertEqual(link.clicks_count, len(urls))

    def test_redirect_preview_with_invalid_alias(self):
        """
        Preview URL with invalid alias should return 404 response.
        """
        response = self.client.get(reverse('url_shortener:alias', args=('blah',)))
        self.assertEqual(response.status_code, 404)

    def test_redirect_preview_with_valid_alias(self):
        """
        Preview URL with valid alias should show a preview containing
        the URL to redirect to.
        """
        link = Link.objects.create(url=URL, alias='b')
        response = self.client.get(reverse('url_shortener:preview', args=('b',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, link.url)
        self.assertEqual(link.clicks_count, 0)


def create_link(url):
    """
    Helper function create a link.
    """
    link = Link.objects.create(url=url)
    link.alias = hash_encode(link.id)
    link.save()
    return link


class TestIndexView(TestCase):

    maxDiff = None

    def assert_link_created(self, response, alias):
        """
        Helper function to check assert that a link was created successfully,
        given the `response` and the expected `alias`
        """
        self.assertRedirects(response, reverse('url_shortener:preview', args=(alias,)))
        self.assertTemplateUsed(response, 'url_shortener/preview.html')
        link = Link.objects.latest('id')
        self.assertEqual(link.url, URL)
        self.assertEqual(link.alias, alias.lower())
        self.assertContains(response, URL)
        self.assertContains(response, alias)

    def test_index_with_no_alias_empty_database(self):
        """
        Submitting index form with no alias specified should
        create a link with auto-generated alias.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
        }, follow=True)
        self.assert_link_created(response, hash_encode(1))

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
        self.assert_link_created(response, hash_encode(latest_link.id + 1))

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
        In case of a conflicting alias, auto-generated alias should be used
        and an appropriate message displayed.
        """
        link1 = create_link(URL)
        link2 = create_link(URL)
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': link1.alias,  # Uh oh, conflicts with the first link
        }, follow=True)
        self.assert_link_created(response, hash_encode(link2.id + 1))
        self.assertContains(response, link1.alias)
        self.assertContains(response, 'exists')

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

    def test_index_with_multiple_uppercase_aliases(self):
        """
        Make sure that aliases are case insensitive, i.e., after having
        created a Link with a given alias, multiple combinations of that
        alias shouldn't be allowed.
        """
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': 'A-Good-Alias',
        }, follow=True)
        self.assert_link_created(response, 'A-Good-Alias')
        response = self.client.post(reverse('url_shortener:index'), {
            'url': URL,
            'alias': 'a-good-alias',
        })
        links = Link.objects.filter(alias__iexact='a-good-alias')
        self.assertEqual(len(links), 1)

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
            'alias': ''.join([hash_encode(i) for i in range(300)]),
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

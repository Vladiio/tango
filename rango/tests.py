from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime
from .models import Category, Page


# helper functions
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(category, title, url, first_visit, last_visit):
    page = Page.objects.get_or_create(category=category,
                                      title=title, url=url)

    page.first_visit = first_visit
    page.last_visit = last_visit
    page.save()
    return page


# tests
class PageMethodTests(TestCase):
    cat = add_cat('test-cat', 1, 1)
    time_now = timezone.now()
    time_month_delta = timezone.timedelta(days=30)

    def test_first_or_last_view_not_in_future(self):
        time_future = self.time_now + self.time_month_delta
        page = Page(category=self.cat, title='test-title',
                    url='test-url', first_visit=time_future,
                    last_visit=time_future)
        page.save()
        self.assertEqual((page.first_visit <= timezone.now()), True)
        self.assertEqual((page.last_visit <= timezone.now()), True)

    def test_last_visit_after_or_equal_first_visit(self):
        last_visit_past = self.time_now - self.time_month_delta
        page = Page(category=self.cat, title='test-title',
                    url='test-url', first_visit=self.time_now,
                    last_visit=last_visit_past)
        page.save()
        self.assertEqual((page.last_visit >= page.first_visit), True)


class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name='Rango Category String')
        cat.save()
        self.assertEqual(cat.slug, 'rango-category-string')


class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 2, 3)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 3)


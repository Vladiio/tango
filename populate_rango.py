import os
from random import randint

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
    'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


VIEWS = 128
LIKES = 64


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {
            "title": "Official Python Tutorial",
            "url":"http://docs.python.org/2/tutorial/",

         },

        {
            "title":"How to Think like a Computer Scientist",
            "url":"http://www.greenteapress.com/thinkpython/",

        },

        {
            "title":"Learn Python in 10 Minutes",
            "url":"http://www.korokithakis.net/tutorials/python/",

        }
     ]

    django_pages = [
        {
            "title":"Official Django Tutorial",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",

        },

        {
            "title":"Django Rocks",
            "url":"http://www.djangorocks.com/",

        },

        {
            "title":"How to Tango with Django",
            "url":"http://www.tangowithdjango.com/",

        }
     ]

    other_pages = [
        {
            "title":"Bottle",
            "url":"http://bottlepy.org/docs/dev/",

        },

        {
            "title":"Flask",
            "url":"http://flask.pocoo.org",

        }
     ]

    pascal_pages = [
        {
            "title":"Lessons",
            "url":"http://learnpascal.ru/",

        },

        {
            "title":"lurkmore",
            "url":"http://lurkmore.to/Pascal",

        }
    ]

    perl_pages = [
        {
            "title":"Wiki",
            "url":"https://ru.wikipedia.org/wiki/Perl",

        },

        {
            "title":"Official",
            "url":"https://www.perl.org/",

        }
    ]

    php_pages = [
        {
            "title":"Wiki",
            "url":"https://ru.wikipedia.org/wiki/PHP",

        },

        {
            "title":"Habr",
            "url":"https://habrahabr.ru/hub/php/",

        }
    ]

    prolog_pages = [
        {
            "title":"Lurkmore",
            "url":"lurkmore.to/Prolog",

        },

        {
            "title":"Habr",
            "url":"https://habrahabr.ru/post/124636/",

        }
    ]

    cats = {
        ("Python", VIEWS, LIKES): {"pages": python_pages},
        ("Django", VIEWS//2, LIKES//2): {"pages": django_pages},
        ("Other Frameworks", VIEWS//4, LIKES//4): {"pages": other_pages},
        ("Pascal", VIEWS, LIKES): {"pages": pascal_pages},
        ("Perl", VIEWS//2, LIKES//4): {"pages": perl_pages},
        ("PHP", VIEWS // 2, LIKES // 2): {"pages": php_pages},
        ("Prolog", VIEWS // 4, LIKES // 4): {"pages": prolog_pages},

     }

     # If you want to add more catergories or pages,
     # add them to the dictionaries above.

     # The code below goes through the cats dictionary, then adds each category,
     # and then adds all the associated pages for that category.
     # if you are using Python 2.x then use cats.iteritems() see
     # http://docs.quantifiedcode.com/python-anti-patterns/readability/
     # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.items():
        c = add_cat(cat[0], cat[1], cat[2])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])

     # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=randint(0, 20)
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

 # Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
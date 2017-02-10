from django.shortcuts import render
from .models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':  category_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by'}
    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['pages'] = Page.objects.filter(category=category)
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)
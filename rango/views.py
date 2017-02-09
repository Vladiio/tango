from django.shortcuts import render
from .models import Category


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':  category_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by'}
    return render(request, 'rango/about.html', context_dict)
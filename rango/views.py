from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Category, Page
from .forms import CategoryForm, PageForm
from .bing_search5 import bing_search


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories':  category_list,
        'pages': pages_list,
    }
    visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context_dict)
    return response


def about(request):
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session.get('visits')}
    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    query = ''
    result_list = []

    if request.method == "POST":

        query = request.POST['query']
        result_list = bing_search(query)
        context_dict['result_list'] = result_list
        context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['pages'] = Page.objects.filter(category=category)
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':

        form = PageForm(request.POST)
        if form.is_valid():

            if category:

                page = form.save(commit=False)
                page.category = category
                page.save()
                return index(request)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def search(request):
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = bing_search(query)

    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})


def track_url(request):
    if request.method == "GET":

        if 'page_id' in request.GET:

            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)

        return redirect('index')


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
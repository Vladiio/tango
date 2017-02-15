from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserProfileForm
from .bing_search5 import bing_search


# view functions

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


def track_url(request):
    """ Increments views and redirect to page"""
    if request.method == "GET":

        if 'page_id' in request.GET:

            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)

        return redirect('index')


@login_required
def user_profile_view(request):
    form = UserProfileForm()
    if request.user:
        return redirect('index')

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')

    return render(request, 'registration/profile_registration.html', {'form': form})


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return redirect('index')

    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', username)
        else:
            print(form.errors)

    return render(request, 'registration/profile.html', {'form': form,
                                                         'selected_user': user,
                                                         'user_profile': user_profile})

# helper functions

def visitor_cookie_handler(request):
    """ Process session last visit and visits counter

        If last visit was more than one day ago,sets
        last visit time to now and increments visits
        counter by 1, else save the same last visit
        time and sets visits counter to 1.
    """

    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    """ Returns the value of cookie in server side"""

    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
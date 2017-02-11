from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from .models import Category, Page
from .forms import CategoryForm, PageForm


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


def register(request):
    registred = False
    if request.method == "POST":

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile_form.save()
            registred = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registred': registred})


def user_login(request):
    context_dict = {}

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user:

            if user.is_active:

                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Your Rango account is disabled.')

        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            context_dict['login_errors'] = 'Invalid username or password'

    return render(request, 'rango/login.html', context_dict)


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

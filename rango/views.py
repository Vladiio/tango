from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import FormView

from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserProfileForm
from .bing_search5 import bing_search


# views

class IndexView(generic.View):
    template_name = 'rango/index.html'

    def get(self, request):
        context = {
            'categories': Category.objects.order_by('-likes')[:5],
            'pages': Page.objects.order_by('-views')[:5],
        }
        visitor_cookie_handler(request)
        return render(request, self.template_name, context)


class AboutView(generic.View):

    def get(self, request):
        visitor_cookie_handler(request)
        context_dict = {'visits': request.session.get('visits')}
        return render(request, 'rango/about.html', context_dict)


class CategoryView(generic.ListView):
    template_name = 'rango/category.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(category=self.category)
        self.query = self.request.GET.get('query', '')
        context['result_list'] = bing_search(self.query)
        return context


@method_decorator(login_required, name='dispatch')
class AddCategoryView(FormView):
    template_name = 'rango/add_category.html'
    form_class = CategoryForm
    success_url = '/rango/'

    def form_valid(self, form):
        form.save(commit=True)
        return super(AddCategoryView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AddPageView(FormView):
    template_name = 'rango/add_page.html'
    form_class = PageForm
    success_url = '/rango/category/'

    def get_context_data(self, **kwargs):
        context = super(AddPageView, self).get_context_data(**kwargs)
        slug = self.kwargs['category_name_slug']
        self.category = Category.objects.get(slug=slug)
        context['category'] = self.category
        return context

    def form_valid(self, form):
        slug = self.kwargs['category_name_slug']
        self.category = Category.objects.get(slug=slug)
        page = form.save(commit=False)
        page.category = self.category
        page.save()
        self.success_url += slug
        return super(AddPageView, self).form_valid(form)


class TrackUrl(generic.View):

    def get(self, request):

        if 'page_id' in request.GET:

            page_id = request.GET['page_id']
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)

        return redirect('index')


@method_decorator(login_required, name='dispatch')
class CreateUserProfile(FormView):
    form_class = UserProfileForm
    template_name = 'registration/profile_registration.html'
    success_url = '/rango/profile/'

    def form_valid(self, form):

        user_profile = form.save(commit=False)
        user_profile.user = self.request.user
        user_profile.save()
        self.success_url += user_profile.user.username
        return super(CreateUserProfile, self).form_valid(form)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return redirect('index')

    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': user_profile.website,
                            'picture': user_profile.picture})

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():

            profile_form.save(commit=True)
            return redirect('profile', user.username)

    return render(request, 'registration/profile.html', {'form': form,
                                                  'selected_user': user,
                                                  'user_profile': user_profile})


class UserListView(generic.ListView):
    template_name = 'rango/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()

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
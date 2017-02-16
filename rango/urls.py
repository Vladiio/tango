from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/', views.AboutView.as_view(), name='about'),

    url(r'^add_category/$',
        views.AddCategoryView.as_view(),
        name='add_category'),


    url(r'^category/(?P<slug>[\w\-]+)/$',
        views.CategoryView.as_view(),
        name='show_category'),


    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/',
        views.AddPageView.as_view(),
        name='add_page'),

    url(r'^goto/$', views.TrackUrl.as_view(), name='goto'),

    url(r'^register_profile/$',
        views.CreateUserProfile.as_view(),
        name='user_profile'),

    url(r'^profile/(?P<username>[\w]+)/$',
        views.profile,
        name='profile'),

    url(r'^user_list/$', views.UserListView.as_view(), name='user_list'),
]
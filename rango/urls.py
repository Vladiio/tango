from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),


    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'),


    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/',
        views.add_page,
        name='add_page'),

    # /rango/goto/1/
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.user_profile_view, name='user_profile'),
    url(r'^profile/(?P<username>[\w]+)/$', views.profile, name='profile'),
]
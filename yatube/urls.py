from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500 # noqa

urlpatterns = [
    path('auth/',
         include('users.urls')),
    path('auth/',
         include('django.contrib.auth.urls')),
    path('admin/',
         admin.site.urls),
    path('about/',
         include('django.contrib.flatpages.urls')),
    path('',
         include('posts.urls')),
]

urlpatterns += [
    path('about/about-us/',
         views.flatpage,
         {'url': 'about/about-us/'},
         name='about'),
    path('about/terms/',
         views.flatpage,
         {'url': 'about/terms/'},
         name='terms'),
    path('about/about-author/',
         views.flatpage,
         {'url': 'about/about-author/'},
         name='about-author'),
    path('about/about-spec/',
         views.flatpage,
         {'url': 'about/about-spec/'},
         name='about-spec'),
]

handler404 = 'posts.views.page_not_found' # noqa
handler500 = 'posts.views.server_error' # noqa

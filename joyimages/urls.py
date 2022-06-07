from django.urls import re_path as url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ImageCreateView,ImageDetailView,ImageListView


urlpatterns = [
    url(r'', views.index, name='index'),

    url(r'register', views.register_new_user, name='register'),
    # url(r'', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'new/image/$', ImageCreateView.as_view(), name='image-add'),
    url(r'(?P<pk>\d+)', ImageDetailView.as_view(), name='image-detail'),
    # url(r'', ImageListView.as_view(), name='image-list'),
    # url(r'comment/add', CommentCreateView.as_view(), name='author-add'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
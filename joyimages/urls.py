from django.urls import re_path as url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from joyimages.views import PostLikeToggle
from .views import ImageCreateView,ImageDetailView,ImageListView


urlpatterns = [
    url(r'register/', views.register_new_user, name='register'),
    url(r'', views.index, name='index'),
    url('post/<id>', views.post_comment, name='comment'),
    # url(r'', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'new/image/$', ImageCreateView.as_view(), name='image-add'),
    url(r'(?P<pk>\d+)', ImageDetailView.as_view(), name='image-detail'),
    url(r'', views.login_required, name='login'),
    # url(r'comment/add', CommentCreateView.as_view(), name='author-add'),
    url('post/<id>', views.post_comment, name='comment'),
    # url('post/<id>/like', PostLikeToggle.as_view(), name='liked'),
    url('like', views.like_post, name='like_post'),
    url('search/', views.search_profile, name='search'),
    url('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    url('follow/<to_follow>', views.follow, name='follow')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
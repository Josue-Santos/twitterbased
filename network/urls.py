
from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("following_index", views.following_index, name="following_index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post",views.post, name="post"),
    path("profile/<str:user>",views.profile,name="profile"),
    path("user/<str:user>",views.user,name="user"),
    path("like/<int:id>",views.like, name="like"),
    path("follow/<int:id>",views.follow, name="follow"),
    path("edit/<int:id>",views.edit, name="edit"),
    path("repost/<int:id>/<str:new_post>",views.repost, name ="repost")

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
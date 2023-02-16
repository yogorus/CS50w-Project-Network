
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('following', views.following_view, name='following'),
    path("profile/<str:username>", views.profile, name='profile'),

    # API routes
    path("profile/<str:username>/follow", views.follow, name='follow'),
    path("new_post", views.new_post, name='new_post'),
    path("posts/<str:section>", views.posts, name='posts')
]

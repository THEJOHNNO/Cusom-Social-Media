
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.submit_post, name="posts"),
    #use u/<username>! This is why it wasn't finding reverse for profile.
    path("u/<username>", views.profile_view, name="profile"),
    #more than one argument
    path("f/<slug:user>/<slug:userId>", views.follow, name="follow"),
    path("following", views.following_view, name="following"),
    #use argument <> for arguments passed into python view function
    path("e/<post>", views.editPost, name="editPost"),
    path("submitEditedPost", views.submitEditedPost, name="submitEditedPost"),
    path("hearted", views.hearted_view, name="hearted")

]
#not a valid view function or pattern name is usually because of a problem with this file or "{% url '' %}"

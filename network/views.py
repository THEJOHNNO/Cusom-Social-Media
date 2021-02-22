from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import *
from django.views.generic import ListView


def index(request):
    user = request.user

    if user in User.objects.all():
        posts = Post.objects.all().order_by("-dateTime")

        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "pageView": page_obj,
            "page_obj": page_obj
        })
    else:
        return HttpResponseRedirect(reverse("network:login"))

@login_required
def following_view(request):
    user = request.user

    follows = UserFollowers.objects.filter(followers=user)
    posts = Post.objects.all().order_by('-dateTime')
    posted = []
    for post in posts:
        for follower in follows:
            if follower.specificUser == post.user:
                posted.append(post)

    if not follows:
        return render(request, 'network/following.html', {'message': "Opps! You don't follow anybody."})


    paginator = Paginator(posted, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "pageView": page_obj,
        "page_obj": page_obj
    })



@csrf_exempt
def profile_view(request, username):
    requestedUser = request.user
    posts = Post.objects.filter(user=username).order_by("-dateTime")
    user = User.objects.get(id=username)

    followersCount = UserFollowers.objects.filter(specificUser=user).count()
    followingCount = UserFollowing.objects.filter(specificUser=user).count()

    followOrNot = "Follow"
    if UserFollowing.objects.filter(specificUser = requestedUser, following = user):
        followOrNot = "Unfollow"
    else:
        followOrNot = "Follow"

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "ProfileUser": user,
        "followersCount": followersCount,
        "followingCount": followingCount,
        "requestedUser": requestedUser,
        "follow": followOrNot
    })

#passed in argument must be the same as url: "a/<>" in url's.py
def follow(request, user, userId):

    userWhoClicks = request.user
    userWhoClicks = User.objects.get(username=userWhoClicks)
    user = User.objects.get(id=userId)

    #use .filter() instead of .get() because .get(), if empty, returns DoesNotExists, whereas filter() returns empty queryset
    if UserFollowing.objects.filter(specificUser = userWhoClicks, following = userId):

        UserFollowing.objects.filter(specificUser = userWhoClicks, following=user).delete()
        UserFollowers.objects.filter(specificUser = user, followers = userWhoClicks).delete()
        return HttpResponseRedirect(reverse("network:profile", args = (userId)))

    else:
        UserFollowing.objects.create(specificUser = userWhoClicks, following = user)
        UserFollowers.objects.create(specificUser = user, followers = userWhoClicks)
        return HttpResponseRedirect(reverse("network:profile", args = (userId)))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

def submit_post(request):
    postBody = request.POST.get("postText")
    user = request.user
    dateAndTime = datetime.datetime.now()

    Post.objects.create(user=user, postContent=postBody, dateTime=dateAndTime, likes=0)

    return HttpResponseRedirect(reverse("network:index"))

@csrf_exempt
def hearted_view(request):

    data = json.loads(request.body)
    currentPostId = data.get("currentPostId")

    userWhoLiked = request.user
    post = Post.objects.get(id=currentPostId)

    if Like.objects.filter(user=userWhoLiked, post=post):

        post.likes -= 1
        post.save()
        Like.objects.get(user=userWhoLiked, post=post).delete()
        return JsonResponse({"postId": currentPostId, "postLikes": post.likes}, status=201)

    #    return JsonResponse({"message": "Problem here"}, status=403)

    else:
        post.likes += 1
        post.save()
        Like.objects.create(user=userWhoLiked, post=post)
        #internal server error 500 will be passed back if there is a problem with this line of code below.
        return JsonResponse({"postId": currentPostId, "postLikes": post.likes}, status=201)

@csrf_exempt
def editPost(request, post):
    post = Post.objects.get(id=post)
    return render(request, "network/editPost.html", {
        "post": post
    })

@csrf_exempt
def submitEditedPost(request):

    data = json.loads(request.body)
    postContent = data.get("postContent")
    postId = data.get("postId")
    post = Post.objects.get(id=postId)
    post.postContent = postContent
    #remember to save to database, or else it won't work!!
    if request.user == post.user:
        post.save()
        return JsonResponse({"message": "You have successfully edited your post!"}, status=201)
    else:
        return JsonResponse({"message": "You are not permitted to edit another user's post. Redirecting you..."}, status=403)

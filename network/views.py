import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post
from .forms import NewPostForm


def index(request):
    return render(request, "network/index.html", {
        'post_form': NewPostForm
    })


def posts(request, section):
    if section == 'all':
        posts = Post.objects.all()
    
    posts = posts.order_by('-date')
    # posts = [post.serialize() for post in posts]
    page = request.GET.get('page', 1) 
    posts_per_page = 2
    p = Paginator(posts, posts_per_page) 

    return render(request, 'network/posts.html', {
        "post_page": p.get_page(page),
        "section": section
    })


def new_post(request):
    if request.method != "POST":
        return JsonResponse({"message: something went wrong!"})

    data = request.body
    data = json.loads(data)
    
    # Get contents of post
    body = data.get('body', '')
    
    new_post = Post(
        author=request.user,
        body=body.split()
    )
    if new_post.is_valid():
        new_post.save()
        return JsonResponse({"Message":"Post created successfully!"}, status=201)
    
    return JsonResponse({"Message":"something went wrong!"}, status=201)


    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

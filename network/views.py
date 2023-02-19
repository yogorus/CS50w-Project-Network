import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from .models import User, Post, Like
from .forms import NewPostForm


def index(request):
    return render(request, "network/index.html", {
        'post_form': NewPostForm
    })


def profile(request, username):
    profile = get_object_or_404(User, username=username)

    # Check if request user follows that profile
    user_is_follower = 1 if request.user in profile.followers.all() else 0  # Will work as a boolean on the frontend

    return render(request, "network/profile.html", {
        "profile": profile,
        'post_form': NewPostForm,
        "user_is_follower": user_is_follower,
        "followers": profile.followers.count(),
        "following": profile.following.count()
    })


@login_required
def following_view(request):
    return render(request, "network/following.html")


@login_required
def follow(request, username):
    
    # Get user who makes the request and the profile he wants to follow
    user = get_object_or_404(User, pk=request.user.id)
    profile = get_object_or_404(User, username=username)
    
    # Prevent user from following himself
    if user == profile:
        return JsonResponse({'message': "You can't follow yourself! That's weird..."})

    if request.method == 'POST':
        # Add that profile to the accounts that this user follows
        user.following.add(profile)
        
        return JsonResponse({'message': 'Success in following!'})
    
    elif request.method == 'DELETE':
        # Make the user to unfollow that account
        user.following.remove(profile)

        return JsonResponse({'message': 'Success in unfollowing!'})

    else:
        return JsonResponse({'message': 'Wrong method!'})


def posts(request, section):
    if section == 'all':
        posts = Post.objects.all()
    
    elif section == 'following':
        users = get_object_or_404(User, pk=request.user.id).following.all()
        posts = Post.objects.filter(author__in=users)
    
    # Query username
    else:
        user = get_object_or_404(User, username=section)
        posts = user.posts
    
    posts = posts.order_by('-date')
    page = request.GET.get('page', 1) 
    posts_per_page = 10
    p = Paginator(posts, posts_per_page) 

    # Return template via fetch
    try:
        return render(request, 'network/posts.html', {
        "post_page": p.get_page(page),
        "section": section
    })
    
    # Return last page if page doesn't exists
    except EmptyPage:
        return render(request, 'network/posts.html', {
        "post_page": p.get_page(p.num_pages),
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
        body=body.strip()
    )
    if new_post.is_valid():
        new_post.save()
        return JsonResponse({"message":"Post created successfully!"}, status=201)
    
    return JsonResponse({"message":"something went wrong!"}, status=201)


def edit_post(request, post_id):
    if request.method != 'PUT':
        return JsonResponse({'message': 'This route only accepts PUT requests!'})
    
    else:
        post = get_object_or_404(Post, pk=post_id)
        
        if post.author != request.user:
            return JsonResponse({'message': "You can't edit someone else's post!"})

        data = request.body
        data = json.loads(data)

        post.body = data.get('body', '')
        
        if post.is_valid():
            post.save()
            return JsonResponse({'message': 'Post edited succesfully!', 'status': 1})
        
        else:
            return JsonResponse({'message': 'Invalid post!', 'status': 0})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'GET':
        # Get all likes for that post and get like from that user if it exists
        try:
            Like.objects.get(liker=request.user, post=post)
            message = 'liked'
        except Like.DoesNotExist:
            message = 'unliked'
        
        return JsonResponse({'message': message, 'likes': post.likes_count()})

    elif request.method == 'POST':
        try:
            Like.objects.get(liker=request.user, post=post).delete()
            return JsonResponse({'message': 'unliked', 'likes': post.likes_count()})
        
        except Like.DoesNotExist:
            Like.objects.create(liker=request.user, post=post)
            return JsonResponse({'message': 'liked', 'likes': post.likes_count()})

    return JsonResponse({'message': 'something went wrong!'})


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

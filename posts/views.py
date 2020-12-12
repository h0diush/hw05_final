from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import render, get_object_or_404
from .models import Comment, Follow, Post, Group
from .forms import CommentForm, PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

User = get_user_model()


@cache_page(20)
def index(request):
    latest = Post.objects.all()
    paginator = Paginator(latest, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page,
         'paginator': paginator
         }
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "group.html",
        {
            "group": group,
            "page": page,
            "paginator": paginator
        }
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        return redirect("index")
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_all = author.posts.all()
    count_post = posts_all.count()
    following = author.following.all() 
    follow= False   
    authors = []
    for us in following:
        author_fol = us.user
        authors.append(author_fol)
    if request.user in authors:
        follow = True
    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'count_post': count_post,
        'paginator': paginator,
        'page': page,
        'follow': follow
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    count_post = author.posts.count()
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    comments_count = post.comments.count()
    form = CommentForm()
    context = {
        'author': author,
        'count_post': count_post,
        'post': post,
        'comments':comments,
        'form': form,
        'comments_count': comments_count
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username=request.user.username, post_id=post_id)
    return render(
        request, 'post_edit.html', {'form': form, 'post': post},
    )

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post=post
        comment.save()
        return redirect('post', username, post_id)
    context =  {'form': form, "post": post, "comments": comments}
    return render(request,"comments.html", context)
   
@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    foll_count = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'foll_count':foll_count}
    return render(
        request, "follow.html", context)

@login_required
def profile_follow(request, username):
    users_viewing_post = get_object_or_404(User, username=username)    
    if request.user != users_viewing_post:
        Follow.objects.get_or_create(author=users_viewing_post, user=request.user)
        return redirect('profile', username)
    return redirect('profile', username)

        

@login_required
def profile_unfollow(request, username):
    users_viewing_post = get_object_or_404(User, username=request.user)
    author_post = get_object_or_404(User, username=username)
    follow_author = Follow.objects.filter(user=users_viewing_post, author=author_post)
    follow = Follow.objects.filter(user=users_viewing_post, author=author_post).exists()
    if follow:
        follow_author.delete()
    return redirect('profile', username)


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500) 


from django.views.generic import TemplateView
from .models import Post
from .models import CustomUser
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


class DeleteNotAllowed(Exception):
    pass


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'pages/user_list.html', {'users': users})


def user_posts(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    posts = user.post_set.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('user-posts', user_id=user.id)
    else:
        form = PostForm()
    return render(request, 'pages/user_detail.html', {'user': user,
                                                      'posts': posts,
                                                      'form': form})


def is_post_owner(user, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return post.user == user


@login_required
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == 'POST':
            if request.user != post.user:
                raise DeleteNotAllowed(
                    "You are not allowed to delete this post.")
            post.delete()
            return redirect('user-posts', user_id=post.user.id)
        return redirect('user-posts', user_id=post.user.id)
    except DeleteNotAllowed as e:
        return HttpResponse(e, status=403)


@login_required
def create_post(request):
    try:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('user-list')
        else:
            form = PostForm()
        return render(request, 'pages/create_post.html', {'form': form})
    except DeleteNotAllowed as e:
        return HttpResponse(e, status=403)

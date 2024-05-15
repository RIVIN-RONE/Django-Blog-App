from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {"post": post}
    return render(request, "blog/post_detail.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, "The post has been created successfully.")
            return redirect("blog-home")
        else:
            messages.error(request, "Please correct the following errors:")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure that only the author can edit the post
    if post.author != request.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect("blog-home")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully.")
            return redirect("post-detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the following errors:")
    else:
        form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"form": form, "post": post})
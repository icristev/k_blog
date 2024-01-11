from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


def index(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 30)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request,
                  'blog/index.html',
                  {'posts': posts})

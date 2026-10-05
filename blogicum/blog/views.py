from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Category, Post
from .constants import POSTS_LIMIT  # ⚠️ Убедись, что здесь нет опечатки!


def index(request):
    """Главная страница: 5 последних опубликованных постов."""
    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )[:POSTS_LIMIT]

    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    # 1. Находим категорию (если нет — сразу 404)
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    # 2. Используем related_name ('posts'), который мы задали в модели.
    # category.posts -> это менеджер запросов для постов этой категории.
    # Нам НЕ нужно писать category=category внутри filter, связь уже есть!
    post_list = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    )

    context = {
        'category': category,
        'post_list': post_list,
    }

    return render(request, 'blog/category.html', context)

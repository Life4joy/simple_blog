from django import template
from django.db.models import Count

from blog.models import Category, Post

register = template.Library()


@register.inclusion_tag('header.html')
def show_category():
    categories = Category.objects.all()[:4]
    return {'categories': categories}


@register.inclusion_tag('sidebar.html')
def trend_latest_com():
    category_count = Category.objects.annotate(pcount=Count('post'))
    trending = Post.objects.filter(featured=True).order_by('views')
    latest = Post.objects.filter(featured=True).order_by('-timestamp')
    by_comments = Post.objects.annotate(commentcount=Count('comments')).order_by('-commentcount')
    context = {
        'trending': trending,
        'latest': latest,
        'by_comments': by_comments,
        'category_count': category_count
    }
    return context

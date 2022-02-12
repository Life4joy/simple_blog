from django.contrib import messages
from django.db.models import Count, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .forms import *

from .models import *


def get_author(user):
    qs = Author.objects.filter(name=user)
    if qs.exists():
        return qs[0]
    return None


class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    allow_empty = False
    
    def get_context_data(self, *, object_list=None, **kwargs):
        latest_posts = Post.objects.filter(featured=True).order_by('-timestamp')[:3]
        context = super(HomeView, self).get_context_data(**kwargs)
        context['latest_posts'] = latest_posts
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'
    allow_empty = False
    context_object_name = "categories"


class PostView(DetailView):
    model = Post
    template_name = 'single-post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class CommentView(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post_id = pk
            form.save()
        return redirect(post.get_absolute_url())


class SearchView(ListView):
    template_name = 'search-results.html'
    paginate_by = 1
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("s"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["search_by"] = self.request.GET.get("s")
        context["s"] = f's={self.request.GET.get("s")}&'
        return context


class CreatePost(CreateView):
    model = Post
    template_name = 'post-create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class Subscribe(View):
    def post(self, request, pk):
        form = SubscribeForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successful')
        return redirect(post.get_absolute_url())


class UpdatePost(UpdateView):
    form_class = PostForm


class DeletePost(DeleteView):
    form_class = PostForm

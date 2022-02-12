from django.urls import reverse
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-list', kwargs={'slug': self.slug})


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return self.name.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_img/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    timestamp = models.TimeField(auto_now_add=True)
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    featured = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'pk': self.pk})

    @property
    def get_comments(self):
        return self.comments.filter(parent__isnull=True)


class Comment(models.Model):
    email = models.EmailField(null=True)
    name = models.CharField(max_length=30)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Subscribe(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

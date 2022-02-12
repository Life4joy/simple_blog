from django.urls import path, include
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('category/<str:slug>/', CategoryView.as_view(), name="category-list"),
    path('post/<int:pk>/', PostView.as_view(), name="post-detail"),
    path('comment/<int:pk>/', CommentView.as_view(), name="add-comment"),
    path('create_post/', CreatePost.as_view(), name="post-create"),
    path('post/<int:pk>/update_post/', UpdatePost.as_view(), name="post-update"),
    path('post/<int:pk>/delete_post/', DeletePost.as_view(), name="post-delete"),
    path('subscribe/<int:pk>/', Subscribe.as_view(), name="subscribe"),
    path('search/', SearchView.as_view(), name="search"),
    path('tinymce/', include('tinymce.urls')),
]

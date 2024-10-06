from django.urls import path
from .views import BlogLikeView, CommentCreateView, blogdetailedview, bloglistCreateView

urlpatterns = [
    path('/', bloglistCreateView.as_view(), name= 'blog'),
    path('/<uuid:pk>/', blogdetailedview.as_view(), name= 'blog'),
    path('/<uuid:pk>/like/', BlogLikeView.as_view(), name='blog-like'),
    path('/<uuid:pk>/comment/', CommentCreateView.as_view(), name='blog-comment-create')
]
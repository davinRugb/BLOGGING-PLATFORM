from .serializers import Blogserializer,CommentSerializer
from rest_framework import generics,permissions,status
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token              
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Blog,Comment
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


class bloglistCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = Blogserializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(Author = self.request.user)
        except IntegrityError as e:
            return Response({
                'message': 'Error in creating Blog',
                'data': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)

        return Response({
            'message': 'Blog created successfully',
            'data': serializer.data
        })
    
class blogdetailedview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all
    serializer_class = Blogserializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Blog, pk=self.kwargs['pk'])
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if isinstance(instance, Response):
            return instance  # Project not found response
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Blog updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if isinstance(instance, Response):
            return instance  # Project not found response
        self.perform_destroy(instance)
        return Response({
            'message': 'Blog deleted successfully',
            'data': {}
        }, status=status.HTTP_204_NO_CONTENT)


class BlogLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.all()

    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user

        if blog.likes.filter(id=user.id).exists():
            blog.likes.remove(user)  # Unlike the blog
            message = 'You have unliked this blog post.'
        else:
            blog.likes.add(user)  # Like the blog
            message = 'You have liked this blog post.'

        return Response({
            'status': message,
            'total_likes': blog.total_likes()  # Assuming you have a method for total likes
        }, status=status.HTTP_200_OK)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blog_id = self.kwargs['pk']
        blog = get_object_or_404(Blog, pk=blog_id)
        serializer.save(user=self.request.user, blog=blog)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Your comment has been successfully posted.",
            "comment": response.data
        }, status=status.HTTP_201_CREATED)
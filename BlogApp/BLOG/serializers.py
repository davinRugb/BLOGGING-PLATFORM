from rest_framework import serializers
from .models import Blog, Comment
from django.contrib.auth import get_user_model

User = get_user_model

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class Blogserializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields = ['id','Title', 'Content', 'Published_Date', 'Category','comments']
        read_only_fields = ['Author','total_likes'] 

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data  # Fetch and serialize comments


class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ['username', 'id']




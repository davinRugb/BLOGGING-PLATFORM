from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Title = models.CharField(max_length=50) 
    Content = models.TextField(max_length=100)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.CharField(max_length=200)
    Published_Date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    
    def __str__(self):
        return self.username
    
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.Title}'
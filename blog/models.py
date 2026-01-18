from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count


class Post(models.Model):
    """Blog Post Model"""
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Content")
    image = models.ImageField(upload_to='blog/posts/', verbose_name="Image")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_likes_count(self):
        """Get total likes count"""
        return self.likes.count()
    
    def get_comments_count(self):
        """Get total comments count"""
        return self.comments.count()


class Comment(models.Model):
    """Blog Comment Model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f"{self.author.username} - {self.post.title}"


class Like(models.Model):
    """Blog Like Model"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name="Post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        unique_together = ('post', 'user')
        verbose_name = "Like"
        verbose_name_plural = "Likes"
    
    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

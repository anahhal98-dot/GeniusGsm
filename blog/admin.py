from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'get_likes_count', 'get_comments_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    fieldsets = (
        ('معلومات المنشور', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('معلومات الناشر', {
            'fields': ('author',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at', 'user']
    readonly_fields = ['created_at']

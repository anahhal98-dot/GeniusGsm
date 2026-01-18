from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating/editing posts"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write the post content here',
                'rows': 8
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add your comment here',
                'rows': 3
            })
        }

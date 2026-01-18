from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


class PostListView(ListView):
    """Display all posts"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.count()
        return context
    
    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        return queryset


class PostDetailView(DetailView):
    """Display post details with comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all()
        context['comment_form'] = CommentForm()
        context['user_liked'] = False
        
        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(
                post=post, 
                user=self.request.user
            ).exists()
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:home')
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post"""
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:home')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required(login_url='login')
def add_comment(request, slug):
    """Add a comment to a post"""
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    
    return redirect('blog:post_detail', slug=slug)


@login_required(login_url='login')
def delete_comment(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    post_slug = comment.post.slug
    
    if request.user == comment.author:
        comment.delete()
    
    return redirect('blog:post_detail', slug=post_slug)


@login_required(login_url='login')
def toggle_like(request, slug):
    """Toggle like/unlike a post"""
    post = get_object_or_404(Post, slug=slug)
    
    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )
    
    if not created:
        like.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': created,
            'total_likes': post.get_likes_count()
        })
    
    return redirect('blog:post_detail', slug=slug)

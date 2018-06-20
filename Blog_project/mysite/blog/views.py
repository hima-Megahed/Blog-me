from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView, UpdateView,
                                    DeleteView)
from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from django.urls import reverse_lazy
from django.utils import timezone

# Create your views here.
###########################################################################
#                      Class Based Views
###########################################################################
class AboutView(TemplateView):
    """docstring for AboutView."""
    template_name = 'about.html'

class PostListView(ListView):
    """docstring for PostListView."""
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    """docstring for PostDetailView."""
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    """docstring for CreatePostView."""
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
    """docstring for UpdatePostView."""
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class DeletePostView(LoginRequiredMixin, DeleteView):
    """docstring for DeletePostView."""
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    """docstring for DraftListView."""
    model = Post
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts_draft'
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


###########################################################################
#                    Functions Based Views
###########################################################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

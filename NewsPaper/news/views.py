from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostList(ListView):
    model = Post
    template_name = 'news.html' #'post_detail.html'#
    context_object_name = 'post'
    queryset = Post.objects.order_by('post_time_create')
    paginate_by = 3
    form_class = PostForm
    #queryset = Post.objects.order_by('time_create')



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['PostCategory'] = Category.objects.all()
        #context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    permission_required = ('news.add_post',)
    form_class = PostForm

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView ):
    template_name = 'post_create.html'
    permission_required = ('news.add_post',)  # ('news.update_post',)
    form_class = PostForm


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post',)  # ('news.delete_post',)
    queryset = Post.objects.all()
    success_url = '/news/'


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'
    ordering = ['post_time_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context





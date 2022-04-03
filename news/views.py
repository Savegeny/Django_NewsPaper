from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.paginator import Paginator

from .models import Post, Category
from .filter import PostFilter
from .forms import PostForm

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    ordering = ["date_create"]
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostSearch(ListView):
    model = Post
    template_name = "search.html"
    context_object_name = "posts"
    ordering = ["date_create"]
    paginate_by = 10
    form_class = PostForm

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class Posts(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    queryset = Post.objects.order_by('-date_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_create"] = datetime.utcnow()
        context["value1"] = None
        return context


class PostDetailView(DetailView):
    template_name = "news_app/post_detail.html"
    queryset = Post.objects.all()


class PostAddView(CreateView):
    template_name = "news_app/post_create.html"
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = "news_app/post_create.html"
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get("pk")
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = "news_app/post_delete.html"
    queryset = Post.objects.all()
    success_url = "/news/"



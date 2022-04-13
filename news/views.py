from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.paginator import Paginator

from .models import Post, BaseRegisterForm, SendMail
from django.views import View
from .filter import PostFilter
from .forms import PostForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail, mail_managers, mail_admins
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class PostAddView(PermissionRequiredMixin, CreateView):
    template_name = "news_app/post_create.html"
    form_class = PostForm
    permission_required = ('news.add_post')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "news_app/post_create.html"
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get("pk")
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "news_app/post_delete.html"
    permission_required = ('news.delete_post')
    queryset = Post.objects.all()
    success_url = "/news/"


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_not_premium'] = not self.request.user.groups.filter(name = 'premium').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class SendMailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_sendmail.html', {})

    def post(self, request, *args, **kwargs):
        post_mail = SendMail(
            date=datetime.strftime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        post_mail.save()

        html_content = render_to_string(
            'created_sendmail.html',
            {
                'post_mail': post_mail,
            }
        )

        send_mail(
            subject=f'{post_mail.client_name}{post_mail.date.strftime("%Y-%M-%d")}',
            message=post_mail.message,
            from_email='savegeny@yandex.ru',
            recipient_list=['savelevgy@gmail.com'],
        )

        return redirect('post_mail:make_mail')
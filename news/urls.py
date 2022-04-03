from django.urls import path
from .views import PostList, PostDetailView, PostAddView, PostUpdateView, PostDeleteView, PostSearch


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('add/', PostAddView.as_view(), name="post_add"),
    path('add/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name="post_search"),
]


from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.ArticleListCreateAPIView.as_view(),
        name='article_list_create'
    ),
    path(
        '<int:pk>/',
        views.ArticleDetailAPIView.as_view(),
        name='article_detail'
    ),
]
from rest_framework import generics

from .models import Article
from .serializers import ArticleSerializer

class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """
    Vue générique pour lister (GET) et créer (POST) des articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue générique pour afficher (GET), mettre à jour (PUT/PATCH)
    et supprimer (DELETE) un article.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
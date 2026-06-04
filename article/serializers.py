from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour convertir les objets Article en JSON.
    """
    class Meta:
        model = Article
        fields =['id', 'title', 'content', 'created_at']  # Champs à inclure dans le JSON
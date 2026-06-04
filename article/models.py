from django.db import models

# Create your models here.
class Article(models.Model):
    """
    Modèle pour représenter un article de blog.
    """
    title = models.CharField(max_length=255)              # Titre limité à 255 caractères
    content = models.TextField()                          # Contenu sans limite de taille
    created_at = models.DateTimeField(auto_now_add=True)  # Ajout automatique de la date

    def __str__(self):
        return self.title  # Représentation en texte de l'objet
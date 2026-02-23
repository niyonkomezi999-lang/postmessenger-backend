from django.db import models
from django.conf import settings 

class MessagePublie(models.Model):
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        date_str = self.date_creation.strftime("%d/%m/%Y") if self.date_creation else "Date inconnue"
        debut_msg = self.contenu[:30] if self.contenu else ""
        return f"[{date_str}] {self.poster.username} : {debut_msg}..."

class Follow(models.Model):
    gagnant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="suiveurs", on_delete=models.CASCADE)
    abonne = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="abonnements", on_delete=models.CASCADE)
    date_abonnement = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('gagnant', 'abonne') 

    def __str__(self):
        return f"{self.abonne.username} suit {self.gagnant.username}"

from django.contrib.auth.models import User
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(MessagePublie, related_name='likes', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # un utilisateur ne peut liker qu'une fois

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(MessagePublie, related_name='comments', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
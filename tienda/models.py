from django.db import models
from django.contrib.auth.models import User


# tabla Post
class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    marca = models.CharField(max_length=50, blank=True, null=False)
    sub_title = models.CharField(max_length=250, blank=True, null=False)
    content = models.TextField()
    img = models.ImageField(upload_to="images/", blank=True, null=True)
    price = models.IntegerField(default=0, null=False)
    amount = models.IntegerField(default=0, null=False)

    # clave_foranea
    usuarioID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title


# tabla Compra
class Compra(models.Model):

    nombreCompra = models.CharField(max_length=100, null=False)
    precioCompra = models.IntegerField(default=0, null=False)

    # clave_foranea
    usuarioID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compra")

    postID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="compra")

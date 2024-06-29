from django.db import models
from django.contrib.auth.models import User


# tabla Post
class Post(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200, blank=True, null=True)
    marca = models.CharField(max_length=100)
    img = models.ImageField(upload_to="posts/", blank=True, null=True)
    price = models.IntegerField(null=False)
    amount = models.PositiveIntegerField()
    content = models.TextField()
    usuarioID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# tabla carroCompra
class Compra(models.Model):

    nombreCompra = models.CharField(max_length=100, null=False)
    precioCompra = models.IntegerField(default=0, null=False)

    # clave_foranea
    usuarioID = models.ForeignKey(User, on_delete=models.CASCADE)

    postID = models.ForeignKey(Post, on_delete=models.CASCADE)

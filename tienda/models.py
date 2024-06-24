from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    marca = models.CharField(max_length=50, blank=True, null=False)
    sub_title = models.CharField(max_length=250, blank=True, null=False)
    content = models.TextField()
    img = models.ImageField(upload_to="images/", blank=True, null=True)
    price = models.IntegerField(default=0, null=False)
    amount = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.title

from django.contrib import admin

from .models import Post, Compra, TransaccionCompra

# Register your models here.

admin.site.register(Post)

admin.site.register(Compra)

admin.site.register(TransaccionCompra)

from django import forms
from .models import Post, Compra, TransaccionCompra

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]  # Campos del modelo User que se van a usar

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("La contrasena no coinside")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(
            self.cleaned_data["password1"]
        )  # Usa set_password para hash seguro
        if commit:
            user.save()
        return user


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "sub_title", "marca", "img", "price", "amount", "content"]


class CompraCreateForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = (
            "nombreCompra",
            "precioCompra",
            "usuarioID",
            "postID",
        )


class TransaccionCreateForm(forms.ModelForm):
    class Meta:
        model = TransaccionCompra
        fields = (
            "totalCompra",
            "cantidadCompra",
            "usuarioID",
        )

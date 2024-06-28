from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, UpdateView, DeleteView
from .forms import PostCreateForm, CompraCreateForm, UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages


from .models import Post, User, Compra
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

# Create your views here.


class TiendaView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            "posts": posts,
        }
        return render(request, "productos\\blog_list_tienda.html", context)


class TusProductos(View):
    def get(self, request, user_id, *args, **kwargs):
        # Filtra los posts que pertenecen al usuario específico
        posts = Post.objects.filter(usuarioID__id=user_id)
        context = {
            "posts": posts,
        }
        return render(request, "productos\\blog_list_user.html", context)


class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostCreateForm()
        context = {"form": form}
        return render(request, "productos\\blog_create.html", context)

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.usuarioID = request.user  # Asigna el post al usuario actual
            post.save()
            return redirect("tienda:home")
        context = {"form": form}
        return render(request, "productos\\blog_create.html", context)


class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {"post": post}
        return render(request, "productos\\blog_detail.html", context)


class BlogDetailViewUser(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {"post": post}
        return render(request, "productos\\blog_detail_user.html", context)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [
        "title",
        "content",
        "marca",
        "sub_title",
        "img",
        "price",
        "amount",
    ]
    template_name = "productos\\blog_update.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("tienda:detailUser", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.usuarioID  # Solo el propietario puede editar


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "productos\\blog_delete.html"
    success_url = reverse_lazy("tienda:home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.usuarioID  # Solo el propietario puede eliminar


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        context = {"form": form}
        return render(request, "usuarios\\user_create.html", context)

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Inicia sesión automáticamente después de registrar
            return redirect(
                reverse_lazy("tienda:login")
            )  # Redirige a la página principal
        else:
            # Si el formulario no es válido, muestra los errores
            context = {"form": form}
            return render(request, "usuarios\\user_create.html", context)


class LoginUser(LoginView):
    template_name = "usuarios\\user_login.html"  # Plantilla para el formulario de login
    redirect_authenticated_user = True  # Redirigir si el usuario ya está autenticado
    success_url = reverse_lazy(
        "tienda:home"
    )  # URL a redirigir después de un inicio de sesión exitoso

    def get_success_url(self):
        """Devuelve la URL a la que redirigir después de un inicio de sesión exitoso."""
        return self.success_url


# salida usuario
class ExitUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Cierra la sesión del usuario
        return redirect(reverse_lazy("tienda:home"))


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "usuarios\\user_update.html"

    def get_success_url(self):
        messages.success(self.request, "Tu perfil ha sido actualizado con éxito.")
        return reverse_lazy("tienda:home")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado exitosamente.")
        return super().form_valid(form)


def agregar_al_carro(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CompraCreateForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuarioID = request.user
            compra.postID = post
            compra.nombreCompra = post.title
            compra.precioCompra = post.price
            compra.save()

    else:
        form = CompraCreateForm()
    return render(request, "productos\\blog_detail.html", {"form": form, "post": post})

    # @login_required
    # def ver_carro(request):
    #     compras = Compra.objects.filter(usuarioID=request.user)
    #     total_precio = sum(compra.precioCompra for compra in compras)
    #     return render(
    #         request,
    #         "productos/ver_carro.html",
    #         {"compras": compras, "total_precio": total_precio},
    #     )

    # @login_required
    # def procesar_compra(request):
    #     compras = Compra.objects.filter(usuarioID=request.user)
    #     if request.method == "POST":
    #         # Aquí podrías agregar la lógica para procesar el pago
    #         # y actualizar el estado de las compras si es necesario.
    #         compras.delete()  # Vacía el carrito después de la compra
    #         return redirect("historial_compras")
    #     total_precio = sum(compra.precioCompra for compra in compras)
    #     return render(
    #         request,
    #         "productos/procesar_compra.html",
    #         {"compras": compras, "total_precio": total_precio},
    #     )

    # @login_required
    # def historial_compras(request):
    #     compras = Compra.objects.filter(usuarioID=request.user)
    #     return render(request, "productos/historial_compras.html", {"compras": compras})

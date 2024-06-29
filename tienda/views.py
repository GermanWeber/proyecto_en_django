from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, UpdateView, DeleteView, ListView, DetailView
from .forms import PostCreateForm, UserCreateForm, TransaccionCompra
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages


from .models import Post, User, Compra
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

# Create your views here.


# ------------------------------------------------------------------------
# VIEWS DE POSTS

# ver todos los Post (usuario)


class TiendaView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            "posts": posts,
        }
        return render(request, "productos\\blog_list_tienda.html", context)


# ver todos los Post (creador)


class TusProductos(View):
    def get(self, request, user_id, *args, **kwargs):
        # Filtra los posts que pertenecen al usuario específico
        posts = Post.objects.filter(usuarioID__id=user_id)
        context = {
            "posts": posts,
        }
        return render(request, "productos\\blog_list_user.html", context)


# creacion de Post


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


# ver detalles del Post (vista usuario)


class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {"post": post}
        return render(request, "productos\\blog_detail.html", context)


# ver detalles del Post (vista creador)


class BlogDetailViewUser(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        context = {"post": post}
        return render(request, "productos\\blog_detail_user.html", context)


# modificar post


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


# eliminar Post


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "productos\\blog_delete.html"
    success_url = reverse_lazy("tienda:home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.usuarioID  # Solo el propietario puede eliminar


# -------------------------------------------------------------------------
# VIEWS DE USERS

# registro de nuevo usuario


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


# login de usuario


class LoginUser(LoginView):
    template_name = "usuarios\\user_login.html"  # Plantilla para el formulario de login
    redirect_authenticated_user = True  # Redirigir si el usuario ya está autenticado
    success_url = reverse_lazy(
        "tienda:home"
    )  # URL a redirigir después de un inicio de sesión exitoso

    def get_success_url(self):
        """Devuelve la URL a la que redirigir después de un inicio de sesión exitoso."""
        return self.success_url


# logout de usuario
class ExitUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)  # Cierra la sesión del usuario
        return redirect(reverse_lazy("tienda:home"))


# modificar usuario


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "usuarios\\user_update.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        messages.success(self.request, "Tu perfil ha sido actualizado con éxito.")
        return reverse_lazy("tienda:usuario_detalle", kwargs={"pk": pk})

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado exitosamente.")
        return super().form_valid(form)


# ver detalles de usuario


class UsuarioDetalleView(DetailView):
    model = User
    template_name = "usuarios\\user_detail.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()
        context["transacciones"] = TransaccionCompra.objects.filter(usuarioID=usuario)
        return context


# ----------------------------------------------------------------------------------
# VIEWS DE COMPRAS

# agragar al carro


@login_required
def agregar_a_compra(request, post_id):
    # Obtener el usuario actual
    usuario = request.user

    try:
        # Obtener el post por su id
        post = Post.objects.get(pk=post_id)

        # Crear un objeto Compra
        nueva_compra = Compra(
            nombreCompra=post.title,
            precioCompra=post.price,
            usuarioID=usuario,
            postID=post,
        )
        nueva_compra.save()

        messages.success(request, "El artículo se ha agregado a tu compra.")
    except Post.DoesNotExist:
        messages.error(request, "El artículo no existe.")

    return redirect("tienda:home")


# mostrar carro de compras


class VerCarro(View):
    def get(self, request, user_id, *args, **kwargs):

        # Obtener las compras del usuario específico
        compras = Compra.objects.filter(usuarioID__id=user_id)

        # Calcular el precio total
        total_precio = sum(compra.precioCompra for compra in compras)
        total_compra = compras.count()

        context = {
            "compras": compras,
            "total_precio": total_precio,
            "total_compra": total_compra,
        }
        return render(request, "compras/carro_compra.html", context)


class BorrarProductoCarro(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Compra
    template_name = "compras/carro_delete.html"

    def get_success_url(self):
        compra = self.get_object()
        return reverse_lazy("tienda:carro", kwargs={"user_id": compra.usuarioID.id})

    def test_func(self):
        compra = self.get_object()
        return self.request.user == compra.usuarioID


class ProcesarCompra(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Obtener todas las compras del usuario
        compras = Compra.objects.filter(usuarioID=request.user)

        if not compras:
            return redirect("tienda:carro", user_id=request.user.id)

        usuario = request.user
        total_compra = sum(compra.precioCompra for compra in compras)
        cantidad = compras.count()

        # Crear una nueva transacción
        nueva_transaccion = TransaccionCompra(
            totalCompra=total_compra,
            cantidadCompra=cantidad,
            usuarioID=usuario,
        )
        nueva_transaccion.save()

        # Eliminar todas las compras después de procesarlas
        compras.delete()

        # Redirigir al historial de transacciones o a una página de confirmación
        return redirect("tienda:historial_transacciones")


class HistorialTransacciones(LoginRequiredMixin, ListView):
    model = TransaccionCompra
    template_name = "compras\historial_compra.html.html"
    context_object_name = "transacciones"

    def get_queryset(self):
        return TransaccionCompra.objects.filter(usuarioID=self.request.user)

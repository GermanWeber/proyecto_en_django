from django.urls import path
from . import views

from .views import (
    BlogCreateView,
    BlogDetailView,
    TiendaView,
    BlogUpdateView,
    BlogDeleteView,
    UserCreateView,
    LoginUser,
    ExitUser,
    TusProductos,
    UserUpdateView,
    BlogDetailViewUser,
)

app_name = "tienda"

urlpatterns = [
    path("", TiendaView.as_view(), name="home"),
    path("create-post/", BlogCreateView.as_view(), name="create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("<int:pk>/user/", BlogDetailViewUser.as_view(), name="detailUser"),
    path("<int:pk>/update-post/", BlogUpdateView.as_view(), name="update"),
    path("<int:pk>/delete-post/", BlogDeleteView.as_view(), name="delete"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", ExitUser.as_view(), name="logout"),
    path("<int:pk>/user-update/", UserUpdateView.as_view(), name="userUpdate"),
    path("<int:user_id>/tus-post/", TusProductos.as_view(), name="tusPost"),
    path(
        "carrito/agregar/<int:post_id>/",
        views.agregar_al_carro,
        name="agregar_al_carro",
    ),
]

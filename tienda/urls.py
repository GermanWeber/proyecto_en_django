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
    VerCarro,
    BorrarProductoCarro,
    ProcesarCompra,
    HistorialTransacciones,
    UsuarioDetalleView,
)

app_name = "tienda"

urlpatterns = [
    # urls de post
    path("", TiendaView.as_view(), name="home"),
    path("create-post/", BlogCreateView.as_view(), name="create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("<int:pk>/user/", BlogDetailViewUser.as_view(), name="detailUser"),
    path("<int:pk>/update-post/", BlogUpdateView.as_view(), name="update"),
    path("<int:pk>/delete-post/", BlogDeleteView.as_view(), name="delete"),
    # -----------------------------------------------------------------------
    # url de usuario
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", ExitUser.as_view(), name="logout"),
    path("usuario/<int:pk>/", UsuarioDetalleView.as_view(), name="usuario_detalle"),
    path("<int:pk>/user-update/", UserUpdateView.as_view(), name="userUpdate"),
    path("<int:user_id>/tus-post/", TusProductos.as_view(), name="tusPost"),
    # ------------------------------------------------------------------------
    # urls de compras y transacciones
    path(
        "agregar_compra/<int:post_id>/", views.agregar_a_compra, name="agregar_compra"
    ),
    path("carro-compra/<int:user_id>", VerCarro.as_view(), name="carro"),
    path("carro/borrar/<int:pk>/", BorrarProductoCarro.as_view(), name="delete_carro"),
    path("carro/procesar/", ProcesarCompra.as_view(), name="procesar_compra"),
    path(
        "historial-transacciones/",
        HistorialTransacciones.as_view(),
        name="historial_transacciones",
    ),
]

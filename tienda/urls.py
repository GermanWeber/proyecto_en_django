from django.urls import path

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
)

app_name = "tienda"

urlpatterns = [
    path("", TiendaView.as_view(), name="home"),
    path("create-post/", BlogCreateView.as_view(), name="create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("<int:pk>/update-post/", BlogUpdateView.as_view(), name="update"),
    path("<int:pk>/delete-post/", BlogDeleteView.as_view(), name="delete"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", ExitUser.as_view(), name="logout"),
    path("<int:user_id>/update-user/", UserUpdateView.as_view(), name="updateUser"),
    path("<int:pk>/tus-post/", TusProductos.as_view(), name="tusPost"),
]

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import api, views


app_name = "inventario"

urlpatterns = [
    path("api/demo/", api.demostracion, name="demo_api"),
    path("api/productos/", api.productos, name="api_productos"),
    path("api/productos/<int:pk>/", api.producto_detalle, name="api_producto_detalle"),
    path("", views.inicio, name="inicio"),
    path("registro/", views.registrar_usuario, name="registro"),
    path(
        "iniciar-sesion/",
        LoginView.as_view(
            template_name="inventario/iniciar_sesion.html",
            next_page="inventario:inicio",
        ),
        name="iniciar_sesion",
    ),
    path(
        "cerrar-sesion/",
        LogoutView.as_view(next_page="inventario:iniciar_sesion"),
        name="cerrar_sesion",
    ),
    path("<str:modulo>/", views.listado, name="listado"),
    path("<str:modulo>/nuevo/", views.crear, name="crear"),
    path("<str:modulo>/<int:pk>/editar/", views.editar, name="editar"),
    path("<str:modulo>/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
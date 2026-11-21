from django.urls import path

from . import api, views


app_name = "inventario"

urlpatterns = [
    path("api/demo/", api.demostracion, name="demo_api"),
    path("api/productos/", api.productos, name="api_productos"),
    path("api/productos/<int:pk>/", api.producto_detalle, name="api_producto_detalle"),
    path("", views.inicio, name="inicio"),
    path("<str:modulo>/", views.listado, name="listado"),
    path("<str:modulo>/nuevo/", views.crear, name="crear"),
    path("<str:modulo>/<int:pk>/editar/", views.editar, name="editar"),
    path("<str:modulo>/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
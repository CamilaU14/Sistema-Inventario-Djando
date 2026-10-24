from django.urls import path

from . import views


app_name = "inventario"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("<str:modulo>/", views.listado, name="listado"),
    path("<str:modulo>/nuevo/", views.crear, name="crear"),
    path("<str:modulo>/<int:pk>/editar/", views.editar, name="editar"),
    path("<str:modulo>/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]
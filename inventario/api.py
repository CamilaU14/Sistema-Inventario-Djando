"""API JSON del módulo de productos del Sistema de Gestión de Inventario."""

import json

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import ProductoForm
from .models import Producto


CAMPOS = tuple(ProductoForm.Meta.fields)
PERMISOS = {
    "GET": "view",
    "HEAD": "view",
    "POST": "add",
    "PUT": "change",
    "PATCH": "change",
    "DELETE": "delete",
}


def comprobar_permiso(request):
    permiso = f"inventario.{PERMISOS[request.method]}_producto"
    if not request.user.has_perm(permiso):
        return JsonResponse(
            {"error": "Inicia sesión con un usuario autorizado para esta operación."},
            status=403,
        )
    return None


def datos_producto(producto):
    return {
        "id": producto.pk,
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio_unitario": str(producto.precio_unitario),
        "stock": producto.stock,
        "estado": producto.estado,
        "categoria": producto.categoria_id,
        "proveedor": producto.proveedor_id,
    }


def guardar_producto(request, producto=None):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Envía datos en formato application/json."}, status=415)

    try:
        datos = json.loads(request.body)
    except (ValueError, RecursionError):
        return JsonResponse({"error": "El contenido JSON no es válido."}, status=400)

    if not isinstance(datos, dict) or not datos:
        return JsonResponse({"error": "Envía un objeto JSON con los campos del producto."}, status=400)

    desconocidos = sorted(datos.keys() - set(CAMPOS))
    if desconocidos:
        return JsonResponse({"error": "Campos desconocidos.", "campos": desconocidos}, status=400)

    if request.method == "PUT":
        faltantes = sorted(set(CAMPOS) - datos.keys())
        if faltantes:
            return JsonResponse({"error": "PUT requiere todos los campos.", "campos": faltantes}, status=400)

    if request.method == "PATCH":
        actuales = datos_producto(producto)
        datos = {**{campo: actuales[campo] for campo in CAMPOS}, **datos}

    formulario = ProductoForm(datos, instance=producto)
    if not formulario.is_valid():
        return JsonResponse({"errores": formulario.errors.get_json_data()}, status=400)

    guardado = formulario.save()
    return JsonResponse(datos_producto(guardado), status=201 if producto is None else 200)


@require_http_methods(["GET", "HEAD", "POST"])
@csrf_protect
def productos(request):
    denegado = comprobar_permiso(request)
    if denegado is not None:
        return denegado
    if request.method in {"GET", "HEAD"}:
        return JsonResponse({"productos": [datos_producto(p) for p in Producto.objects.all()]})

    try:
        with transaction.atomic():
            return guardar_producto(request)
    except IntegrityError:
        return JsonResponse({"error": "El registro entra en conflicto con los datos actuales."}, status=409)


@require_http_methods(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@csrf_protect
def producto_detalle(request, pk):
    denegado = comprobar_permiso(request)
    if denegado is not None:
        return denegado

    if request.method in {"GET", "HEAD"}:
        producto = Producto.objects.filter(pk=pk).first()
        if producto is None:
            return JsonResponse({"error": "Producto no encontrado."}, status=404)
        return JsonResponse(datos_producto(producto))

    try:
        with transaction.atomic():
            producto = Producto.objects.select_for_update().filter(pk=pk).first()
            if producto is None:
                return JsonResponse({"error": "Producto no encontrado."}, status=404)
            if request.method == "DELETE":
                producto.delete()
                return HttpResponse(status=204)
            return guardar_producto(request, producto)
    except (ProtectedError, IntegrityError):
        return JsonResponse({"error": "La operación entra en conflicto con los datos actuales."}, status=409)


@require_http_methods(["GET"])
def demostracion(request):
    denegado = comprobar_permiso(request)
    if denegado is not None:
        return denegado
    return render(request, "inventario/demo_api.html")

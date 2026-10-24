from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CategoriaForm, ProductoForm, ProveedorForm
from .models import Categoria, Producto, Proveedor


# Configuración de los tres módulos del inventario.
MODULOS = {
    "categorias": {
        "modelo": Categoria,
        "formulario": CategoriaForm,
        "titulo": "Categorías",
        "campos_busqueda": ["nombre"],
    },
    "proveedores": {
        "modelo": Proveedor,
        "formulario": ProveedorForm,
        "titulo": "Proveedores",
        "campos_busqueda": ["nit", "nombre"],
    },
    "productos": {
        "modelo": Producto,
        "formulario": ProductoForm,
        "titulo": "Productos",
        "campos_busqueda": ["codigo", "nombre"],
    },
}


def obtener_modulo(modulo):
    """Busca la configuración del módulo solicitado."""
    from django.http import Http404

    if modulo not in MODULOS:
        raise Http404("El módulo solicitado no existe.")

    return MODULOS[modulo]


def inicio(request):
    return redirect("inventario:listado", modulo="productos")


@require_http_methods(["GET"])
def listado(request, modulo):
    configuracion = obtener_modulo(modulo)
    registros = configuracion["modelo"].objects.all()

    if modulo == "productos":
        registros = registros.select_related("categoria", "proveedor")

    busqueda = request.GET.get("q", "").strip()

    if busqueda:
        condiciones = Q()

        for campo in configuracion["campos_busqueda"]:
            condiciones |= Q(**{f"{campo}__icontains": busqueda})

        registros = registros.filter(condiciones)

    # Usamos el ID para mantener un orden estable entre páginas.
    registros = registros.order_by("nombre", "pk")
    paginador = Paginator(registros, 10)
    pagina = paginador.get_page(request.GET.get("page"))

    return render(
        request,
        "inventario/listado.html",
        {
            "modulo": modulo,
            "titulo": configuracion["titulo"],
            "pagina": pagina,
            "busqueda": busqueda,
        },
    )


@require_http_methods(["GET", "POST"])
def crear(request, modulo):
    configuracion = obtener_modulo(modulo)
    formulario = configuracion["formulario"](
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Registro creado correctamente.")
        return redirect("inventario:listado", modulo=modulo)

    return render(
        request,
        "inventario/formulario.html",
        {
            "modulo": modulo,
            "titulo": f"Nuevo registro - {configuracion['titulo']}",
            "formulario": formulario,
        },
    )


@require_http_methods(["GET", "POST"])
def editar(request, modulo, pk):
    configuracion = obtener_modulo(modulo)
    registro = get_object_or_404(configuracion["modelo"], pk=pk)

    formulario = configuracion["formulario"](
        request.POST if request.method == "POST" else None,
        instance=registro,
    )

    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Registro actualizado correctamente.")
        return redirect("inventario:listado", modulo=modulo)

    return render(
        request,
        "inventario/formulario.html",
        {
            "modulo": modulo,
            "titulo": f"Editar registro - {configuracion['titulo']}",
            "formulario": formulario,
        },
    )


@require_http_methods(["GET", "POST"])
def eliminar(request, modulo, pk):
    configuracion = obtener_modulo(modulo)
    registro = get_object_or_404(configuracion["modelo"], pk=pk)

    if request.method == "POST":
        try:
            registro.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este registro porque tiene "
                "productos asociados.",
            )

        return redirect("inventario:listado", modulo=modulo)

    return render(
        request,
        "inventario/confirmar_eliminar.html",
        {
            "modulo": modulo,
            "titulo": "Confirmar eliminación",
            "registro": registro,
        },
    )

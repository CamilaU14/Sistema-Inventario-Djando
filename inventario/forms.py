from django import forms

from .models import Categoria, Proveedor, Producto


class EstiloFormulario(forms.ModelForm):
    """Aplica las clases de Bootstrap a los campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            else:
                campo.widget.attrs["class"] = "form-control"


class CategoriaForm(EstiloFormulario):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "estado"]
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "estado": "Estado",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class ProveedorForm(EstiloFormulario):
    class Meta:
        model = Proveedor
        fields = [
            "nit",
            "nombre",
            "telefono",
            "correo",
            "direccion",
            "estado",
        ]
        labels = {
            "nit": "NIT",
            "nombre": "Nombre",
            "telefono": "Teléfono",
            "correo": "Correo electrónico",
            "direccion": "Dirección",
            "estado": "Estado",
        }


class ProductoForm(EstiloFormulario):
    class Meta:
        model = Producto
        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "categoria",
            "proveedor",
            "precio_unitario",
            "stock",
            "estado",
        ]
        labels = {
            "codigo": "Código",
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "categoria": "Categoría",
            "proveedor": "Proveedor",
            "precio_unitario": "Precio unitario",
            "stock": "Cantidad disponible",
            "estado": "Estado",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "precio_unitario": forms.NumberInput(
                attrs={"min": "0", "step": "0.01"}
            ),
            "stock": forms.NumberInput(attrs={"min": "0"}),
        }
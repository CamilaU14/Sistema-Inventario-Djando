from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


ESTADOS = [
    ("Activo", "Activo"),
    ("Inactivo", "Inactivo"),
]


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS,
        default="Activo",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS,
        default="Activo",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock = models.PositiveIntegerField(default=0)
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS,
        default="Activo",
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    class Meta:
        ordering = ["nombre", "id"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
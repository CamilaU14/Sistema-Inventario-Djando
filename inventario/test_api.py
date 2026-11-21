from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Categoria, Producto, Proveedor


class ProductoAPITest(TestCase):
    def setUp(self):
        usuario = get_user_model().objects.create_superuser(username="aprendiz")
        self.client.force_login(usuario)
        categoria = Categoria.objects.create(nombre="Herramientas")
        proveedor = Proveedor.objects.create(
            nit="123", nombre="Proveedor de prueba", telefono="123", correo="prueba@example.com"
        )
        self.lista = "/api/productos/"
        self.datos = {
            "codigo": "TOR-12",
            "nombre": "Caja de tornillos",
            "descripcion": "",
            "precio_unitario": "8500.00",
            "stock": 20,
            "estado": "Activo",
            "categoria": categoria.pk,
            "proveedor": proveedor.pk,
        }

    def test_ciclo_crud(self):
        respuesta = self.client.post(self.lista, self.datos, content_type="application/json")
        self.assertEqual(respuesta.status_code, 201)
        pk = respuesta.json()["id"]
        detalle = f"{self.lista}{pk}/"
        self.assertEqual(self.client.get(self.lista).json()["productos"][0]["id"], pk)
        self.assertEqual(self.client.get(detalle).json()["stock"], 20)

        respuesta = self.client.patch(detalle, {"stock": 15}, content_type="application/json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["nombre"], self.datos["nombre"])
        reemplazo = {**self.datos, "nombre": "Caja grande de tornillos", "stock": 25}
        respuesta = self.client.put(detalle, reemplazo, content_type="application/json")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Producto.objects.get(pk=pk).stock, 25)
        self.assertEqual(self.client.delete(detalle).status_code, 204)
        self.assertEqual(self.client.get(detalle).status_code, 404)

    def test_datos_invalidos(self):
        datos = {**self.datos, "precio_unitario": "-1.00"}
        respuesta = self.client.post(self.lista, datos, content_type="application/json")
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("precio_unitario", respuesta.json()["errores"])
        self.assertFalse(Producto.objects.exists())

    def test_solicitud_sin_permiso(self):
        self.client.logout()
        self.assertEqual(self.client.get(self.lista).status_code, 403)

    def test_demostracion_renderiza(self):
        respuesta = self.client.get("/api/demo/")
        self.assertContains(respuesta, "Prueba de la API de productos")
        self.assertContains(respuesta, 'data-api="/api/productos/"')
        self.assertContains(respuesta, 'name="csrfmiddlewaretoken"')

# API de productos del Sistema de Gestión de Inventario

**Evidencia GA7-220501096-AA3-EV01**  
María Camila Usma Ocampo · ADSO · Ficha 3336222

Implementé una API que permite consultar, registrar, editar y eliminar productos mediante HTTP. Django utiliza el formulario del inventario para validar la información y el modelo Producto para guardarla. La API entrega JSON y reutiliza la base de datos configurada en el proyecto.

## Abrir el proyecto completo en Windows

1. Extrae el ZIP y abre en VS Code la carpeta `Sistema_Inventario_Django`, donde está `manage.py`.
2. Enciende MySQL en Laragon. La configuración del proyecto busca la base `sistema_inventario` en localhost, puerto 3306. Si aún no tienes la base, créala en DBeaver. Si ya existe, puedes usarla con los datos que tienes en tu equipo.
3. En la terminal PowerShell de VS Code, crea el entorno virtual e instala las dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

4. Aplica las migraciones y enciende Django:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Estos comandos usan el Python de `.venv` directamente. El ZIP contiene el código y las migraciones. Los datos de MySQL se encuentran en tu equipo.

## Rutas

| Método | Ruta | Resultado |
| --- | --- | --- |
| GET | /api/productos/ | 200 con un objeto que contiene la lista en `productos` |
| GET | /api/productos/{id}/ | 200 con el producto solicitado |
| POST | /api/productos/ | 201 con el producto creado |
| PUT | /api/productos/{id}/ | 200 con el producto actualizado mediante todos los campos |
| PATCH | /api/productos/{id}/ | 200 con el producto actualizado mediante los campos enviados |
| DELETE | /api/productos/{id}/ | 204 sin cuerpo |

Se devuelve 400 para datos inválidos, 403 cuando faltan permisos o la comprobación CSRF falla, 404 para un producto inexistente, 405 para un método no admitido, 409 si ocurre un conflicto al guardar o eliminar, y 415 si el cuerpo tiene un tipo de contenido distinto de JSON.

## Demostración en el navegador

1. Inicia sesión en http://127.0.0.1:8000/admin/ con tu superusuario. Si aún no tienes uno, ejecuta `manage.py createsuperuser` con el Python del entorno virtual.
2. Registra una categoría, un proveedor y un producto de prueba desde el CRUD web.
3. Abre http://127.0.0.1:8000/api/demo/. La pantalla usa JavaScript y Fetch para consultar la lista con GET y actualizar el stock del producto seleccionado con PATCH.
4. Abre la pestaña Red de las herramientas del navegador para ver cada solicitud, su método, código HTTP y respuesta JSON.

### Arquitectura y comunicación

El SGI tiene una arquitectura web cliente-servidor. El navegador presenta las plantillas HTML de Django y se comunica por HTTP. La pantalla de práctica utiliza Fetch API para llamar a las dos rutas JSON de la tabla. Django controla permisos, valida los datos con ProductoForm y accede a MySQL mediante su ORM. MySQL conserva los productos y sus relaciones con categorías y proveedores.

El ejemplo de clase consultaba usuarios de JSONPlaceholder. En mi ejercicio utilicé productos de mi propia base de datos: GET muestra el inventario y PATCH guarda el cambio de stock. La aplicación web existente sigue usando sus formularios HTML.

Para POST o PUT envía `codigo`, `nombre`, `descripcion`, `precio_unitario`, `stock`, `estado`, `categoria` y `proveedor`. El precio puede enviarse como texto decimal, por ejemplo `"8500.00"`. La categoría y el proveedor son identificadores de registros existentes.

## Enviar los cambios al repositorio

Desde tu carpeta original con Git, después de copiar y probar los archivos de la evidencia:

```powershell
git add inventario/api.py inventario/urls.py inventario/test_api.py inventario/templates/inventario/demo_api.html README_GA7-AA3-EV01.md
git commit -m "Implementa API REST de productos para evidencia GA7-AA3-EV01"
git push
```

Repositorio base  
https://github.com/CamilaU14/Sistema-Inventario-Djando

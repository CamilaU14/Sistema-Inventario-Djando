# Sistema de Gestión de Inventario
María Camila Usma Ocampo - Ficha 3336222
Evidencia GA7-220501096-AA2-EV02

## Alcance
CRUD de categorías, proveedores y productos, búsqueda, paginación de diez registros y confirmación de eliminación. Las relaciones protegen categorías y proveedores asociados a productos. No incluye movimientos, reportes ni autenticación de usuarios del inventario.

## Ejecutar en Windows
1. Instalar Python 3.13 y MySQL 8 (en el ejercicio se utilizó Laragon con MySQL 8.4.3).
2. Encender MySQL y crear en DBeaver la base sistema_inventario con utf8mb4. También puede ejecutar:
   CREATE DATABASE sistema_inventario CHARACTER SET utf8mb4;
3. Abrir esta carpeta, donde se encuentra manage.py, en Visual Studio Code.
4. Ejecutar uno por uno en PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

5. Abrir http://127.0.0.1:8000/. Detener con Ctrl+C.

La conexión en config/settings.py utiliza localhost, puerto 3306, usuario root y contraseña vacía para el entorno local del ejercicio. Si su MySQL usa otros datos, ajuste esos campos localmente. La base y sus datos no están dentro de este ZIP: migrate crea las tablas vacías. Registre primero una categoría, después un proveedor y finalmente un producto.
Bootstrap se carga por CDN y necesita Internet para los estilos.

## Estructura
- config/: configuración y rutas principales.
- inventario/models.py: tablas y relaciones.
- inventario/forms.py: formularios y validaciones.
- inventario/views.py: GET, POST, CRUD y paginación.
- inventario/urls.py: rutas de los módulos.
- inventario/templates/inventario/: plantillas HTML.
- inventario/migrations/: estructura de la base reproducible.

## Pruebas
Las pruebas manuales y las capturas se encuentran en el informe adjunto. tests.py conserva la plantilla inicial y no contiene pruebas automatizadas. La revisión del paquete validó sintaxis, configuración y comportamiento mediante una base temporal SQLite; no sustituye las pruebas locales con MySQL.

## Ajustes de esta copia
Se corrigió America/Bogata por America/Bogota en settings.py y se retiró __pycache__. No se modificó el CRUD. Configuración académica local: DEBUG=True y clave de desarrollo, sin preparación para producción.

## Repositorio
https://github.com/CamilaU14/Sistema-Inventario-Djando
El repositorio publicado precede a los ajustes y a este README. Para sincronizar, copie README.md y la corrección de TIME_ZONE a su proyecto original y ejecute:

```powershell
git add README.md config/settings.py
git commit -m "Documenta instalacion y corrige zona horaria"
git push
```

# AgroValle — Paso 1: Configuración inicial del proyecto

Documento de registro de todo lo realizado para dejar el proyecto **AgroValle** funcionando: qué se hizo, en qué archivo, por qué y para qué.

> ⚠️ **Importante:** este documento contiene la contraseña de la base de datos. **No lo subas a un repositorio público de GitHub.** Si lo guardas dentro de la carpeta del proyecto, agrégalo al `.gitignore`.

---

## 1. Datos generales del proyecto

| Elemento | Valor |
|---|---|
| Nombre del proyecto | AgroValle |
| Materia | Desarrollo de Software 1 |
| Objetivo | Sistema web de cultivos (papa, maíz, zanahoria, etc.) con seguimiento por etapas, recomendaciones con dosis y comercialización de la cosecha |
| Lenguaje | Python |
| Framework | Django |
| Base de datos | PostgreSQL (administrada con pgAdmin) |
| Carpeta del proyecto | `agrovalle` |

### Credenciales

| Dato | Valor |
|---|---|
| Contraseña de pgAdmin / PostgreSQL | `00005` |
| Nombre de la base de datos | `agrovalle_db` |
| Usuario de la base de datos | `agrovalle_user` |
| Contraseña del usuario de la base de datos | la asignada al crear `agrovalle_user` (en este documento se asume `00005`) |
| Superusuario de Django | el creado con `createsuperuser` (paso 11) |

### Decisión de arquitectura: un solo proyecto Django

Se decidió **no separar** el frontend y el backend en dos carpetas/proyectos distintos.

**Por qué:**
- Es más rápido de desarrollar en el tiempo de un semestre.
- El inicio de sesión, los permisos y los formularios ya vienen resueltos en Django.
- Se despliega en un solo servidor.
- Las páginas generadas en el servidor cargan más livianas, lo que favorece a productores con internet lento.

**Cómo se mantiene ordenado:** el frontend vive en las carpetas `templates/` (HTML) y `static/` (CSS, JS, imágenes), y el backend en las apps (`cuentas`, `cultivos`, `siembras`, `mercado`). Si en el futuro se necesita una app móvil, se puede agregar Django REST Framework al mismo proyecto sin rehacer nada.

---

## 2. Estructura final de carpetas

```
agrovalle/
├── venv/                ← entorno virtual (no se sube a GitHub)
├── config/              ← configuración general del proyecto
│   ├── __init__.py
│   ├── settings.py      ← ajustes (base de datos, apps, idioma, etc.)
│   ├── urls.py          ← rutas principales
│   ├── asgi.py
│   └── wsgi.py
├── cuentas/             ← app: usuarios y roles
├── cultivos/            ← app: catálogo de cultivos, etapas y recomendaciones
├── siembras/            ← app: siembras de cada productor y su avance
├── mercado/             ← app: publicaciones de cosecha y pedidos
├── templates/           ← frontend: páginas HTML
├── static/              ← frontend: archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── .env                 ← datos secretos (no se sube a GitHub)
├── .gitignore           ← lista de lo que Git debe ignorar
└── manage.py            ← herramienta para administrar el proyecto
```

---

## 3. Pasos realizados

### Paso 1 — Crear la carpeta del proyecto

**Dónde:** terminal (CMD o PowerShell).

```bash
mkdir agrovalle
cd agrovalle
```

**Para qué:** tener un lugar único donde vivirá todo el código del sistema.

---

### Paso 2 — Crear y activar el entorno virtual

**Dónde:** terminal, dentro de `agrovalle`.

```bash
python -m venv venv
venv\Scripts\activate
```

**Qué hace:**
- `python -m venv venv` crea la carpeta `venv/`, que es una instalación de Python aislada solo para este proyecto.
- `venv\Scripts\activate` activa ese entorno. Se nota porque aparece `(venv)` al inicio de la línea en la terminal.

**Por qué:** si se instalan las librerías en el Python general de la computadora, distintos proyectos pueden chocar entre sí por versiones diferentes. El entorno virtual mantiene las librerías de AgroValle separadas.

**Para qué:** que cada integrante del grupo tenga exactamente las mismas librerías y el proyecto funcione igual en todas las computadoras.

> Cada vez que se abra una terminal nueva para trabajar, hay que volver a ejecutar `venv\Scripts\activate`.

---

### Paso 3 — Instalar las librerías necesarias

**Dónde:** terminal, con el entorno virtual activado.

```bash
pip install django "psycopg[binary]" python-decouple
```

| Librería | Para qué sirve |
|---|---|
| `django` | El framework con el que se construye todo el sistema web |
| `psycopg[binary]` | El conector que permite a Django comunicarse con PostgreSQL |
| `python-decouple` | Permite leer la contraseña y otros datos secretos desde el archivo `.env`, en lugar de escribirlos dentro del código |

---

### Paso 4 — Crear el proyecto Django

**Dónde:** terminal.

```bash
django-admin startproject config .
```

**Qué hace:** crea la carpeta `config/` (con `settings.py`, `urls.py`, etc.) y el archivo `manage.py`.

**Por qué se llama `config`:** porque esa carpeta solo contiene la configuración general; el nombre deja claro su propósito y lo distingue de las apps.

**Por qué el punto (`.`) al final:** indica que el proyecto se cree en la carpeta actual. Sin el punto, Django crearía una carpeta extra (`agrovalle/config/config/`), lo que complica la estructura.

---

### Paso 5 — Crear las apps

**Dónde:** terminal.

```bash
python manage.py startapp cuentas
python manage.py startapp cultivos
python manage.py startapp siembras
python manage.py startapp mercado
```

**Qué hace:** crea una carpeta por app, cada una con sus archivos base (`models.py`, `views.py`, `admin.py`, etc.).

**Por qué dividir en apps:** cada app tiene una sola responsabilidad. Así el código queda ordenado y el grupo puede repartirse el trabajo sin pisarse.

| App | Responsabilidad |
|---|---|
| `cuentas` | Usuarios y roles (productor, comprador, administrador/técnico) |
| `cultivos` | Catálogo técnico: cultivos, sus etapas (con días fijos) y recomendaciones por etapa (producto y dosis) |
| `siembras` | Lo que cada productor tiene sembrado, en qué etapa va, confirmaciones de avance y extensiones de días |
| `mercado` | Publicación de la cosecha a la venta y pedidos de los compradores |

---

### Paso 6 — Crear las carpetas del frontend

**Dónde:** terminal.

```bash
mkdir templates static static\css static\js static\img
```

| Carpeta | Para qué |
|---|---|
| `templates/` | Guardar las páginas HTML del sistema |
| `static/css/` | Hojas de estilo (diseño, colores) |
| `static/js/` | Código JavaScript para interacciones en el navegador |
| `static/img/` | Imágenes y logos |

**Por qué:** separar visualmente el frontend del backend dentro del mismo proyecto, según la decisión de arquitectura.

---

### Paso 7 — Crear la base de datos en PostgreSQL

**Dónde:** pgAdmin (Query Tool), conectado con la contraseña `00005`.

```sql
CREATE DATABASE agrovalle_db;
CREATE USER agrovalle_user WITH PASSWORD '00005';
ALTER DATABASE agrovalle_db OWNER TO agrovalle_user;
```

**Qué hace cada línea:**
1. Crea la base de datos donde se guardará toda la información del sistema.
2. Crea un usuario específico para el proyecto.
3. Le da a ese usuario la propiedad de la base de datos, para que Django pueda crear y modificar tablas.

**Por qué un usuario propio y no el usuario `postgres`:** `postgres` es el administrador total del servidor. Usar un usuario limitado al proyecto es más seguro: si algo falla, solo afecta a `agrovalle_db`.

---

### Paso 8 — Crear el archivo `.env`

**Dónde:** archivo nuevo `agrovalle/.env` (junto a `manage.py`).

```
DB_NAME=agrovalle_db
DB_USER=agrovalle_user
DB_PASSWORD=00005
DB_HOST=localhost
DB_PORT=5432
```

| Variable | Significado |
|---|---|
| `DB_NAME` | Nombre de la base de datos |
| `DB_USER` | Usuario con el que Django se conecta |
| `DB_PASSWORD` | Contraseña de ese usuario |
| `DB_HOST` | Dónde está PostgreSQL (`localhost` = en la misma computadora) |
| `DB_PORT` | Puerto de PostgreSQL (5432 es el predeterminado) |

**Por qué:** las contraseñas no deben escribirse dentro del código. Si el código se sube a GitHub, cualquiera podría verlas.

**Para qué:** cada integrante puede tener su propio `.env` con sus propios datos de conexión, sin modificar el código compartido.

---

### Paso 9 — Modificar `config/settings.py`

**Dónde:** archivo `agrovalle/config/settings.py`.

Este archivo es el "panel de control" del proyecto. Se hicieron los siguientes cambios:

#### 9.1 Importar `config` de decouple

```python
from pathlib import Path
from decouple import config
```

**Para qué:** poder leer los datos del archivo `.env`.

#### 9.2 Registrar las apps en `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuentas',
    'cultivos',
    'siembras',
    'mercado',
]
```

**Por qué:** crear una app con `startapp` no basta; Django solo reconoce las apps que están en esta lista.

**Para qué:** que Django lea sus modelos, cree sus tablas y muestre sus páginas.

#### 9.3 Indicar dónde están las plantillas

Dentro del bloque `TEMPLATES`, se cambió:

```python
'DIRS': [],
```

por:

```python
'DIRS': [BASE_DIR / 'templates'],
```

**Para qué:** que Django busque las páginas HTML en la carpeta `templates/` creada en el paso 6.

#### 9.4 Conectar con PostgreSQL

Se reemplazó el bloque `DATABASES` (que venía con SQLite) por:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

**Por qué:** Django usa SQLite por defecto, que sirve para pruebas pero no para un sistema real con varios usuarios. PostgreSQL es más robusto y es la base de datos elegida por el grupo.

**Para qué:** que toda la información del sistema se guarde en `agrovalle_db`. Los valores se leen del `.env` con `config(...)`.

#### 9.5 Idioma y zona horaria

```python
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/La_Paz'
```

**Para qué:**
- `es`: el panel de administración y los mensajes de Django aparecen en español.
- `America/La_Paz`: las fechas y horas se registran con la hora de Bolivia. Esto es clave para el motor de etapas, que calcula días desde la siembra.

#### 9.6 Archivos estáticos

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Para qué:** que Django encuentre los archivos CSS, JS e imágenes de la carpeta `static/`.

---

### Paso 10 — Crear el archivo `.gitignore`

**Dónde:** archivo nuevo `agrovalle/.gitignore` (junto a `manage.py`).

```
venv/
.env
__pycache__/
*.pyc
```

| Línea | Por qué se ignora |
|---|---|
| `venv/` | Es pesado y cada integrante crea el suyo en su computadora |
| `.env` | Contiene la contraseña |
| `__pycache__/` y `*.pyc` | Archivos temporales que Python genera automáticamente |

**Para qué:** al subir el proyecto a GitHub, Git no sube estos archivos.

---

### Paso 11 — Crear las tablas, el superusuario y probar

**Dónde:** terminal, con el entorno virtual activado.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| Comando | Qué hace | Para qué |
|---|---|---|
| `migrate` | Crea en `agrovalle_db` las tablas que Django necesita (usuarios, sesiones, permisos) | Confirmar que la conexión con PostgreSQL funciona y dejar lista la base |
| `createsuperuser` | Crea un usuario administrador (pide nombre, correo y contraseña) | Poder entrar al panel de administración |
| `runserver` | Levanta el servidor de desarrollo | Ver el sistema en el navegador |

**Resultado obtenido:**
- En `http://127.0.0.1:8000` aparece el cohete de Django → el proyecto está bien instalado. ✅
- En `http://127.0.0.1:8000/admin` se puede entrar con el superusuario y el panel aparece en español.

---

## 4. Resumen de archivos creados y modificados

| Archivo | Acción | Para qué |
|---|---|---|
| `venv/` | Creado (automático) | Entorno aislado de Python |
| `config/` y `manage.py` | Creados (automático) | Configuración y administración del proyecto |
| `cuentas/`, `cultivos/`, `siembras/`, `mercado/` | Creados (automático) | Las cuatro apps del sistema |
| `templates/`, `static/` | Creados (manual) | Frontend |
| `.env` | Creado (manual) | Datos secretos de conexión |
| `config/settings.py` | **Modificado** | Apps, plantillas, PostgreSQL, idioma, zona horaria, estáticos |
| `.gitignore` | Creado (manual) | Evitar subir archivos privados o innecesarios |
| Base de datos `agrovalle_db` | Creada en pgAdmin | Guardar la información del sistema |

---

## 5. Cómo volver a levantar el proyecto cada día

```bash
cd agrovalle
venv\Scripts\activate
python manage.py runserver
```

Para detener el servidor: `Ctrl + C` en la terminal.

---

## 6. Errores comunes y solución

| Error | Causa probable | Solución |
|---|---|---|
| `'django-admin' no se reconoce...` | El entorno virtual no está activado | Ejecutar `venv\Scripts\activate` |
| `password authentication failed` | La contraseña del `.env` no coincide con la de `agrovalle_user` | Revisar `DB_PASSWORD` en `.env` |
| `connection refused` | PostgreSQL no está encendido | Abrir pgAdmin o iniciar el servicio de PostgreSQL |
| `UndefinedValueError: DB_NAME not found` | El `.env` no está junto a `manage.py` o tiene otro nombre | Verificar ubicación y que se llame exactamente `.env` |
| `permission denied for schema public` | El usuario no es dueño de la base de datos | Ejecutar en pgAdmin: `ALTER DATABASE agrovalle_db OWNER TO agrovalle_user;` |

---

## 7. Próximo paso

**Paso 2 — Modelos del catálogo (app `cultivos`):** definir en `cultivos/models.py` las tablas de Cultivo, Etapa (con días fijos) y Recomendación (producto, dosis y si es obligatoria), y registrarlas en el panel de administración para que los estudiantes de agropecuaria puedan cargar la información técnica.
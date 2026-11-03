# Agro_Valle 🌱

Sistema integral de gestión agrícola desarrollado con arquitectura desacoplada (**Backend** en Django REST Framework y **Frontend** en React + Vite + Tailwind CSS).

---

## 🛠️ Tecnologías del Proyecto

| Componente | Tecnología | Detalle |
| :--- | :--- | :--- |
| **Base de Datos** | PostgreSQL | BD: `agrovalle` en `localhost:5432` |
| **Backend** | Django 6.1 + DRF | API REST modular en carpeta `/backend` |
| **Autenticación** | SimpleJWT | Tokens Bearer (`/api/token/`) |
| **Frontend** | React 19 + Vite | SPA moderna en carpeta `/frontend` |
| **Estilos** | Tailwind CSS | Diseño responsivo para campo y oficina |
| **Entorno Virtual** | Python 3.14 (`.venv/`) | Dependencias aisladas en la raíz |

---

## 🚀 Cómo Iniciar el Proyecto

### 1. Iniciar el Backend (Django)
Abre una terminal en la raíz del proyecto:
```powershell
# 1. Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# 2. Entrar a la carpeta del backend
cd backend

# 3. Iniciar el servidor de desarrollo
python manage.py runserver
```
- **API URL:** `http://localhost:8000/api/`
- **Panel Administrativo:** `http://localhost:8000/admin/`
- **Credenciales Superusuario inicial:**
  - Usuario: `admin`
  - Contraseña: `admin123`

### 2. Iniciar el Frontend (React)
Abre una segunda terminal:
```powershell
# 1. Entrar a la carpeta del frontend
cd frontend

# 2. Iniciar el servidor Vite
npm run dev
```
- **Aplicación Web:** `http://localhost:5173/`

---

## 📁 Estructura de Carpetas

```text
Agro_Valle/
│── .venv/               # Entorno virtual de Python
│── backend/             # Proyecto Django REST Framework
│   ├── config/          # Configuración principal (settings, urls, wsgi)
│   ├── requirements/    # Requerimientos por entorno (base, dev, prod)
│   ├── .env             # Variables de entorno y credenciales
│   ├── .env.example     # Plantilla de variables
│   └── manage.py
│── frontend/            # Aplicación React + Vite
│   ├── src/
│   │   ├── api/axios.js # Cliente HTTP con soporte para JWT
│   │   ├── App.jsx      # Pantalla principal / Dashboard
│   │   └── index.css    # Tailwind CSS
│   ├── package.json
│   └── vite.config.js
│── .gitignore           # Exclusiones de Git (seguridad y dependencias)
└── README.md            # Documentación general
```

---

## 📌 Estado Actual

- [x] Entorno virtual `.venv` configurado e inicializado.
- [x] Dependencias instaladas en backend y frontend.
- [x] Conexión a PostgreSQL (`agrovalle`) establecida y migraciones ejecutadas.
- [x] Configuración de autenticación JWT y CORS entre frontend y backend.
- [x] Estructura desacoplada en `backend/` y `frontend/`.
- [ ] **Siguiente paso:** Implementación de modelos y módulos del negocio (Cultivos, Inventario, Cosechas, Ventas, etc.).


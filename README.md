# 🏨 Milmoteles — Buscador & Comparador Inteligente de Moteles

> **Plataforma web geolocalizada para buscar, comparar y reservar moteles en Medellín con base en la mejor relación calidad-precio y actualización transparente de tarifas.**

---

## 👥 Equipo de Desarrollo (Aprendices SENA)
- **Esteban Cardona Ospina**
- **David Sierra Higuita**
- **Jesus Armando De la Rosa Diaz**

---

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.14 + Django 5.1 + Django REST Framework (DRF)
- **Base de Datos:** PostgreSQL en la nube vía [Supabase](https://supabase.com) (con soporte local MySQL/Postgres)
- **Driver de BD:** `psycopg` (Psycopg 3 binario) con soporte de Connection Pooling (Supavisor)
- **Seguridad:** Aislamiento de secretos con `django-environ`, encriptación moderna con `Argon2`
- **Testing:** `pytest` + `pytest-django` + `pytest-cov` (100% cobertura en modelos)
- **Frontend (Próxima fase):** React + Vite

---

## 🚀 Guía de Instalación y Puesta en Marcha (Paso a Paso)

Sigue estos sencillos pasos para abrir y ejecutar **Milmoteles** directamente desde tu IDE (VS Code / Antigravity):

### 1. Abrir el proyecto en el IDE
1. Clona el repositorio si aún no lo tienes:
   ```bash
   git clone https://github.com/Cardonaesteban/Milmoteles.git
   ```
2. Abre tu IDE y selecciona **File ➔ Open Folder...** (Archivo ➔ Abrir carpeta).
3. Selecciona la carpeta **`Milmoteles`**.

---

### 2. Abrir la Terminal Integrada del IDE
- Presiona el atajo: **`Ctrl + Ñ`** (o ve al menú superior: **Terminal ➔ New Terminal**).

---

### 3. Entrar a `backend/` y crear el entorno virtual
En la terminal integrada del IDE, ejecuta:
```bash
cd backend
python -m venv venv
```

---

### 4. Vincular el entorno virtual al IDE
1. Presiona **`Ctrl + Shift + P`** en el IDE.
2. Escribe y selecciona: **`Python: Select Interpreter`**.
3. Elige la opción que contiene el entorno virtual:  
   `Python 3.14 (.'venv': venv) .\backend\venv\Scripts\python.exe`
> *Tip: A partir de este momento, cada vez que abras una terminal en el IDE con `Ctrl + Ñ`, el entorno virtual `(venv)` se activará automáticamente sin comandos adicionales.*

---

### 5. Instalar dependencias en el IDE
En la terminal integrada del IDE, ejecuta:
```bash
pip install -r requirements-dev.txt
```

---

### 6. Configurar el archivo `.env` desde el Explorador del IDE
1. En el panel izquierdo del IDE (Explorador de archivos), abre la carpeta **`backend`**.
2. Haz clic derecho sobre **`.env.example`** ➔ **Copy** (Copiar) y luego **Paste** (Pegar) en la misma carpeta.
3. Cambia el nombre de la copia a **`.env`**.
4. Ábrelo en el editor y asegúrate de tener la conexión a Supabase con la contraseña del equipo:
   ```env
   DATABASE_URL=postgresql://postgres.unlraxgwtzckxxthlwwe:TU_CONTRASEÑA@aws-0-us-east-2.pooler.supabase.com:5432/postgres
   ```
5. Guarda con **`Ctrl + S`**.

---

### 7. Aplicar migraciones a la Base de Datos
En la terminal integrada del IDE:
```bash
python manage.py migrate
```

---

### 8. Ejecutar las pruebas unitarias (Quality Gate)
En la terminal integrada del IDE:
```bash
pytest
```
*Todas las pruebas deben pasar en verde (16/16 con 100% de cobertura).*

---

### 9. Iniciar el servidor local de desarrollo
En la terminal integrada del IDE:
```bash
python manage.py runserver
```
- **API Backend:** `http://127.0.0.1:8000/`
- **Panel Administrativo:** `http://127.0.0.1:8000/admin/`

---

## 📁 Estructura del Proyecto
```plaintext
Milmoteles/
├── README.md                 # Guía general de instalación y documentación
├── rules.md                  # Reglas obligatorias de arquitectura y seguridad
├── .env.example              # Plantilla pública de variables de entorno
├── .gitignore                # Exclusiones de Git (seguridad)
└── backend/                  # Núcleo del Backend en Django
    ├── .env                  # Variables privadas de entorno (NO se sube a Git)
    ├── .env.example          # Plantilla específica de variables del backend
    ├── manage.py             # CLI de administración de Django
    ├── requirements.txt      # Dependencias de producción
    ├── requirements-dev.txt  # Dependencias de desarrollo y testing
    ├── pytest.ini            # Configuración de suite de pruebas
    ├── core/                 # Configuración del proyecto Django
    │   └── settings/         # Configuración modular (base, local, test)
    └── apps/
        └── moteles/          # Módulo de Moteles y Tarifas
            ├── models.py     # Modelos Motel y Tarifa (Validaciones estrictas)
            ├── admin.py      # Panel de administración de Django
            └── tests/        # Pruebas unitarias automatizadas con pytest
```

---

## 🔒 Reglas Principales de Seguridad y Calidad
1. **[ENV-VARS/SECRETS]**: Queda estrictamente prohibido subir contraseñas o API Keys a Git. Toda credencial se gestiona mediante el archivo `.env` local.
2. **[Validation Gates]**: No se avanza a nuevos hitos o características sin que la suite de pruebas de `pytest` esté 100% en verde.
3. **[INPUT-VAL/SANITIZE]**: Precios estrictamente mayores a cero (`> 0`) y normalización obligatoria de duraciones de tarifas.

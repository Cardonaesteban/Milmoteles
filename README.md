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

Sigue estos sencillos pasos para clonar y ejecutar el backend de **Milmoteles** en tu computadora:

### 1. Clonar el repositorio
Abre tu terminal y clona el proyecto:
```bash
git clone https://github.com/Cardonaesteban/Milmoteles.git
cd Milmoteles
```

---

### 2. Entrar a la carpeta del backend
```bash
cd backend
```

---

### 3. Crear y activar el entorno virtual

#### En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Si PowerShell te muestra error de directivas de ejecución, ejecuta antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`).*

#### En Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### En Linux o macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Instalar dependencias
Con el entorno virtual activado (`(venv)` al inicio de la terminal), instala todas las librerías necesarias:
```bash
pip install -r requirements-dev.txt
```

---

### 5. Configurar el archivo de variables de entorno (`.env`)
Por estándares de ciberseguridad, las contraseñas nunca se suben a GitHub. Debes crear tu archivo local `.env`:

1. Crea una copia de la plantilla:
   - **En Windows:** `copy .env.example .env`
   - **En Linux/Mac:** `cp .env.example .env`
2. Abre el archivo `.env` recién creado en `backend/.env`.
3. Solicita al administrador del equipo la cadena de conexión de Supabase o utiliza la siguiente estructura con las credenciales del equipo:
   ```env
   # Configuración de Base de Datos en Supabase
   DATABASE_URL=postgresql://postgres.unlraxgwtzckxxthlwwe:TU_CONTRASEÑA@aws-0-us-east-2.pooler.supabase.com:5432/postgres
   ```
4. Guarda el archivo `.env`.

---

### 6. Aplicar las migraciones a la Base de Datos
Para sincronizar las tablas de moteles y tarifas con Supabase:
```bash
python manage.py migrate
```

---

### 7. Ejecutar las pruebas unitarias (Quality Gate)
Para verificar que toda la lógica de negocio, duraciones y precios esté funcionando al 100%:
```bash
pytest
```
*Deberás ver todas las pruebas en verde con 100% de cobertura en `apps.moteles`.*

---

### 8. Iniciar el servidor local de desarrollo
```bash
python manage.py runserver
```
El backend estará disponible en: **`http://127.0.0.1:8000/`**  
Panel administrativo: **`http://127.0.0.1:8000/admin/`**

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

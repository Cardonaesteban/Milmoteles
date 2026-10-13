#  REGLAS Y ESTÁNDARES IMPERATIVOS DE CÓDIGO & SEGURIDAD

## 1. DATOS Y CONTEXTO DEL PROYECTO
- **Aprendiz / Responsable:** Esteban Cardona Ospina, David Sierra Higuita, Jesus Armando De la Rosa DIaz
- **Nombre de la Aplicación:** Milmoteles

### A. Documento de Requerimientos de Producto (`prd.md`):
  # Product Requirements Document (PRD)
  
  ## 1. Visión y Propósito
  **Problema a resolver:** Facilitar a las personas la búsqueda del mejor costo-beneficio al momento de elegir un motel, ofreciendo un acceso rápido y sencillo a buenas opciones locales.
  **Propuesta de Valor:** Un buscador y comparador de moteles geolocalizado, centrado en optimizar la relación calidad-precio y la facilidad de uso.
  **Métrica de Éxito (KPI):** GMV Comparado (Nº de reservas realizadas × precio promedio de la reserva).
  
  ## 2. Usuarios y Roles (RBAC)
  *   **Administrador:** Acceso total al sistema (dueños de la plataforma).
  *   **Usuario Cliente (Registrado):** Puede buscar, aplicar filtros, ver referencias, guardar favoritos, ver historial y realizar reservas.
  *   **Usuario Invitado (Anónimo):** Solo puede buscar, aplicar filtros y comparar precios.
  *   **Propietario de Motel:** Puede registrar su establecimiento, gestionar información, actualizar precios/disponibilidad y ver métricas de reservas.
  
  ## 3. Funcionalidades Clave (MVP)
  *   **Buscador y Filtros:** Búsqueda por sectores en Medellín. Filtros por ubicación, precio, duración, servicios, categoría y disponibilidad. Ordenamiento por precio, distancia, popularidad o relación costo-beneficio.
  *   **Comparador Normalizado:** Los precios deben mostrarse en la misma unidad de tiempo (ej. 3 horas, amanecida, etc.).
  *   **Geolocalización:** Mostrar moteles cercanos (opcional, pidiendo permisos al usuario).
  *   **Ficha del Motel:** Mostrar precios, calificación, promociones, reseñas y fecha exacta de última actualización de tarifas.
  *   **Gestión de Cuentas:** Registro y login (con modal rápido si se intenta una acción protegida).
  *   **Acciones de Conversión:** Redirección a la página de reservas y sistema de favoritos.
  
  ## 4. Restricciones y Exclusiones (Límites)
  *   **Diseño:** Obligatoriamente *Mobile-First*. Responsive (celular, tablet, PC).
  *   **Integración de Precios:** Capacidad de recibir precios por API, Base de Datos o carga manual.
  *   **Comparación Estricta:** No comparar tarifas con duraciones diferentes como si fueran equivalentes.
  *   **SEO:** Las fichas de los moteles deben ser indexables por motores de búsqueda.
  *   **Criterio Bloqueante de Lanzamiento:** NUNCA mostrar un precio o disponibilidad que el sistema no pueda identificar como válido, actualizado y asociado a una duración específica.
  
  ## 5. Casos Límite (Edge Cases) y Validaciones
  *   Manejo de estados sin resultados (moteles no encontrados).
  *   Cambios de precio en tiempo real mientras el usuario compara.
  *   Validaciones estrictas: Precio > 0, duraciones válidas, fechas coherentes (no en el pasado).
  *   Control de permisos (un propietario no puede editar un motel ajeno).

### B. Documento de Requerimientos Técnicos (`trd.md`):
  # Technical Requirements Document (TRD)
  
  ## 1. Stack Tecnológico y Arquitectura
  *   **Arquitectura:** Cliente-Servidor Desacoplado.
  *   **Frontend:** React (HTML, CSS, JavaScript).
  *   **Backend:** Django (Python) exponiendo una API REST (Django REST Framework).
  *   **Base de Datos:** MySQL (modelado inicial vía Workbench).
  
  ## 2. Modelo de Datos y Seguridad (ERD)
  *   **Entidades Principales:** Usuarios, Moteles, Habitaciones, Tarifas, Dueños, Reservas.
  *   **Seguridad de Datos:** `Django Object-Level Permissions`. Garantiza a nivel de código que cada propietario solo tiene permisos de escritura sobre sus propios registros (filas) en MySQL.
  
  ## 3. Integración de APIs y Manejo de Secretos
  *   **Servicios Externos:** Google Maps o Mapbox para geolocalización, trazado de rutas y cálculo de distancias por sectores.
  *   **Gestión de Secretos:** Variables de entorno (`.env`) en local y *Gestor nativo del proveedor de Hosting* (ej. variables de entorno de Render/Railway) en producción. Cero secretos en el código fuente.
  
  ## 4. Estrategia de Pruebas (Testing) y Validación
  *   **Validación de Datos:** Enfoque *Híbrido*. Frontend validado tempranamente con **Zod**, y Backend con validación estricta a través de **Serializadores nativos (DRF)**.
  *   **Suite de Pruebas:** Pruebas unitarias obligatorias. `pytest` para lógica de precios/fechas en Django y `Jest` para componentes de UI en React.
  
  ## 5. DevOps, Despliegue y Observabilidad
  *   **Despliegue:** Plataforma PaaS (Render, Railway o similares) para despliegues ágiles de backend y base de datos.
  *   **Observabilidad:** Integración con **Datadog** o **New Relic** (APM) para monitorizar el rendimiento de la API, tiempos de respuesta de MySQL y captura de errores en tiempo real.

### C. Flujo de Usuario y Experiencia (`userflow.md`):
  # User Flow y Experiencia de Interfaz
  
  ## 1. Punto de Partida y Estados de Sesión
  *   **Entry Point:** Pantalla principal (Home) con acceso directo al buscador por sectores y filtros clave.
  *   **Usuario Anónimo:** Puede navegar libremente por el Home, realizar búsquedas, utilizar los filtros y comparar resultados.
  *   **Usuario Autenticado:** Tiene acceso a la reserva, guardado de favoritos y visualización de historial.
  
  ## 2. Bifurcaciones y Escenarios Alternativos (Edge Cases)
  *   **Intento de Acción Protegida:** Si un usuario anónimo intenta guardar un favorito o reservar, **NO** se le saca del flujo. Se despliega un *Modal de Login rápido* para que inicie sesión y continúe exactamente donde estaba.
  *   **Manejo de Errores Externos:** Si la redirección al motel falla o el precio caduca, se lanza un mensaje de error claro indicando la falla y permitiendo recargar la oferta.
  
  ## 3. Estados de la Interfaz (UI States)
  *   **Estado de Carga (Loading):** Uso exclusivo de *Skeleton Loaders* para mantener la estructura visual de la pantalla mientras se traen los moteles y tarifas desde Django.
  *   **Estado Vacío (Empty State):** Si una búsqueda con filtros no arroja resultados, se mostrará un mensaje amigable ("No hay moteles que apliquen a estos filtros") acompañado de sugerencias automáticas de moteles en zonas cercanas.
  
  ## 4. Cierre y Feedback (Success Loopback)
  *   **Tras la Reserva/Redirección:** Al finalizar la acción y volver a la app, el usuario recibirá una confirmación de éxito ("Felicitaciones") y se le presentará un sistema de calificación por estrellas para evaluar la experiencia de la reserva o del motel.

### D. Plan de Ejecución y Roadmap (`plan.md`):
  # Plan de Desarrollo y Roadmap
  
  ## 1. Alcance y Estrategia MVP
  *   **Objetivo de Fase 1:** Construir el "Núcleo Mínimo" al 80% de funcionalidad operativa. Esto incluye: Búsqueda, filtrado, comparación, vista de detalle del motel, autenticación y flujo de reserva.
  *   **Exclusiones del MVP (Para Fases 2 y 3):** Chatbot, sistemas de notificaciones complejas u otras funcionalidades "nice-to-have" que no bloqueen la reserva.
  
  ## 2. Estructura de Hitos (Enfoque Vertical / End-to-End)
  Se desarrollará por características completas (Frontend + Backend conectado).
  *   **Hito 1:** Listado base de moteles, base de datos de consulta, y tarjeta de información (UI + DB + API).
  *   **Hito 2:** Motor de búsqueda y filtros combinados (Ubicación, Precios, Duración) con validación estricta de actualización de tarifas.
  *   **Hito 3:** Sistema de Autenticación, registro de dueños de moteles y panel de gestión básico.
  *   **Hito 4:** Flujo de Conversión, redirecciones de reserva y guardado de favoritos (requiere autenticación).
  
  ## 3. Puertas de Calidad y Ejecución (IA Constraints)
  *   **Criterio de Parada (Validation Gates):** Cobertura de pruebas en verde. La IA o el desarrollador no puede avanzar al siguiente hito sin que los tests de `Jest` (React) y `pytest` (Django) del hito actual pasen exitosamente.
  *   **Tamaño de Tareas:** *Micro-tareas (Atómicas).* Desarrollo guiado paso a paso (ej. 1. Crear modelo SQL -> 2. Crear Serializador -> 3. Crear Endpoint -> 4. Crear componente UI).
  
  ## 4. Estrategia de Despliegue
  *   **Vibe Deploying:** Desarrollo local inicial. El pase a la nube (Render/PaaS) solo se ejecutará cuando el MVP (ese 80% del núcleo) esté completamente consolidado y funcional en el entorno de desarrollo local.

---

## 2. REGLAS TÉCNICAS Y DE SEGURIDAD MANDATORIAS (68 ACTIVADAS)
- **[INPUT-VAL/SANITIZE]**: Validación y sanitización estricta de todos los inputs (Zod, Joi, DOMPurify).
- **[ENV-VARS/SECRETS]**: Secretos, tokens y API keys aislados exclusivamente en variables de entorno (.env).
- **[HASH-CRYPT/ARGON2]**: Contraseñas cifradas con algoritmos modernos (Argon2id o bcrypt, nunca MD5/SHA1).
- **[AUTH-JWT/RBAC]**: Autenticación robusta y control de acceso basado en roles (RBAC) en cada endpoint.
- **[CSP-HEADERS/HELMET]**: Cabeceras HTTP seguras (Helmet, CSP restrictiva, HSTS, X-Content-Type-Options).
- **[RATE-LIMIT/DDOS]**: Limitación de tasa (Rate Limiting) en endpoints críticos y protección anti-fuerza bruta.
- **[CORS-POL/ORIGIN]**: Configuración restrictiva de CORS limitando orígenes explícitos en producción.
- **[FILE-SEC/UPLOAD-VAL]**: Validación estricta de tipo MIME, extensión, magic bytes y cuota en subida de archivos.
- **[ERR-MASK/LOG-SEC]**: Ocultar stack traces y errores de servidor en producción; logs sanitizados sin datos sensibles.
- **[CSRF-PROT]**: Protección contra falsificación de peticiones en sitios cruzados (tokens anti-CSRF / SameSite cookies).
- **[GDPR/RGPD]**: Página y cláusulas de política de privacidad y protección de datos personales.
- **[T&C]**: Página de Términos y Condiciones de uso del servicio.
- **[HTTP 404]**: Página de error 404 personalizada con enlace de retorno amigable.
- **[HTTP 500]**: Página de error 500 para fallos inesperados de servidor sin exponer código interno.
- **[TYP (Thank You Page)]**: Página de confirmación/agradecimiento tras completar acciones o registros.
- **[CS (Coming Soon)]**: Sección o modal de estado para funciones en construcción o casos de estudio.
- **[FAQ]**: Sección de preguntas frecuentes con respuestas desplegables (accordion).
- **[A/U (About Us)]**: Página o sección 'Sobre Nosotros' con propósito, visión y equipo de trabajo.
- **[BC (Breadcrumbs)]**: Migas de pan (Breadcrumbs) para navegación jerárquica en rutas profundas.
- **[NAV]**: Barra de navegación principal fija/accesible con links funcionales.
- **[IL (Internal Linking)]**: Enlaces internos coherentes entre vistas, productos y documentación.
- **[FT (Footer)]**: Footer informativo con copyright, enlaces legales, mapa de sitio y contacto.
- **[Sitemap XML]**: Generación de sitemap.xml actualizado para rastreo eficiente de motores de búsqueda.
- **[Robots.txt]**: Archivo robots.txt configurado para indexación y protección de rutas privadas.
- **[Title Tag]**: Títulos descriptivos y únicos (50-60 caracteres) por cada vista o ruta.
- **[MD (Meta Description)]**: Meta Description optimizada (150-160 caracteres) en cada página para CTR.
- **[ALT (Atributos de Imagen)]**: Atributos alt obligatorios y descriptivos en todas las imágenes.
- **[JSON-LD]**: Datos estructurados Schema.org (JSON-LD) para rich snippets en Google.
- **[OG Image]**: Metadatos Open Graph (og:image, og:title) y Twitter Cards para previews en redes.
- **[NAP]**: Consistencia en Nombre, Dirección y Teléfono (Name, Address, Phone) visible.
- **[CF (Contact Form)]**: Formulario de contacto funcional con validación y estados de envío claros.
- **[VLD (Live Validation)]**: Validación inmediata en tiempo real con mensajes de error comprensibles.
- **[SLA]**: Respuesta automática o indicador de tiempo de espera (SLA) tras enviar mensajes.
- **[CMP (Cookies Banner)]**: Banner de consentimiento de cookies y almacenamiento local (CMP/Cookies).
- **[CTA Hero]**: Call-to-Action prominente, claro y contrastado en la sección Hero principal.
- **[CTA Rep]**: Reiteración estratégica de CTAs a lo largo del scroll en puntos clave.
- **[Sticky CTA]**: Botón de acción flotante/fijo en vista móvil para facilitar conversión rápida.
- **[NL (Newsletter)]**: Formulario de suscripción a boletín o newsletter con validación de email.
- **[Live Chat]**: Canal de atención directa o soporte (WhatsApp / widget de chat).
- **[SP (Social Proof)]**: Prueba social (Social Proof: testimonios, valoraciones o casos reales).
- **[Trust Badges]**: Sellos de confianza, pasarelas seguras (SSL, Stripe) y certificaciones visibles.
- **[RWD (Responsive Web Design)]**: Diseño totalmente adaptativo validado en breakpoints móviles, tablets y desktop.
- **[M-NAV (Mobile Navigation)]**: Menú móvil intuitivo (hamburguesa o barra inferior) con fácil cierre.
- **[Favicon]**: Favicon multiplataforma (SVG, PNG 32x32, Apple Touch Icon) configurado.
- **[STT (Scroll To Top)]**: Botón accesible 'Volver Arriba' en páginas con desplazamiento largo.
- **[Dark Mode]**: Soporte de modo oscuro y contraste WCAG sin pérdida de legibilidad.
- **[I18N]**: Preparación para internacionalización y soporte multiidioma en la interfaz.
- **[PB (Proportion & Blocks)]**: Proporciones y espaciado armónico de bloques según sistema de diseño.
- **[Home Link]**: Logo del encabezado con enlace de retorno inmediato a la página de inicio.
- **[Tel Link]**: Enlaces telefónicos configurados con protocolo 'tel:' para marcación móvil.
- **[Mailto Link]**: Enlaces de correo configurados con protocolo 'mailto:' y asunto predeterminado.
- **[No Overflow]**: Prevención absoluta de scroll horizontal accidental en todos los viewports.
- **[Wireframe Cleanup]**: Limpieza de textos temporales (Lorem Ipsum), imágenes rotas y botones inertes.
- **[WPO (Web Performance)]**: Optimización web (minificación, compresión gzip/brotli, formatos WebP/AVIF).
- **[CWV (Core Web Vitals)]**: Cumplimiento de Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP interactivo rápido).
- **[SSL/HTTPS]**: Forzar tráfico 100% cifrado sobre HTTPS con redirección automática y HSTS.
- **[Smooth Scroll]**: Desplazamiento suave (scroll-behavior: smooth) en enlaces de anclaje interno.
- **[UI Feedback]**: Feedback inmediato ante acciones de usuario (notificaciones toast, spinners, loaders).
- **[CSS Hover]**: Microinteracciones y estados visuales :hover y :focus-visible en elementos clicables.
- **[Skeleton Screen]**: Pantallas de carga esqueletizadas para evitar saltos de layout en peticiones async.
- **[CSS Transitions]**: Transiciones fluidas (150ms-300ms) sin saltos bruscos en cambios de estado.
- **[Hero Animation]**: Animación sutil de entrada en la primera pantalla visible para retención.
- **[RRSS Links]**: Enlaces a perfiles oficiales de redes sociales con target='_blank' y rel='noopener'.
- **[Social Share]**: Botones para compartir contenido directamente en redes sociales y mensajería.
- **[Embed Video]**: Incrustación de video optimizada con lazy loading y reproductor responsivo.
- **[Pricing Matrix]**: Tabla o tarjetas de precios con comparación clara de planes y suscripción.
- **[Version Control]**: Control de versiones con Git siguiendo conventional commits y ramas limpias.
- **[COPY & 404 Audit]**: Auditoría ortográfica, gramatical, consistencia de tono y chequeo de rutas sin 404 rotos.


---

## 3. PROHIBICIONES Y MANDATOS ABSOLUTOS DE SEGURIDAD
1. Queda PROHIBIDO exponer API Keys, contraseñas o secretos en el código fuente. Usar exclusivamente variables `.env`.
2. Todo input del usuario DEBE ser sanitizado obligatoriamente antes de ser procesado o guardado.
3. No utilizar algoritmos de hashing obsoletos (ej. MD5, SHA1). Usar Argon2id o bcrypt.
4. Ocultar stack traces y errores técnicos de servidor en producción.
5. La IA NO PUEDE finalizar ninguna tarea sin verificar explícitamente el cumplimiento de cada regla de este archivo.

# 📘 Documento de Diseño – Hojas de Personaje Inteligentes para D&D

## 📌 1. Resumen del Proyecto

**Nombre Tentativo:** *EchoSheet*  
**Objetivo:**  
Crear una aplicación web que permita a jugadores de Dungeons & Dragons (D&D 5e) generar, gestionar y conversar con sus personajes mediante una ficha inteligente que se rellena automáticamente, sugiere mejoras y permite un diario conversacional.

---

## 🎯 2. Objetivos Funcionales

- Generar hojas de personaje a partir de información básica.
- Sugerir habilidades, hechizos y mejoras óptimas al subir de nivel.
- Proporcionar una interfaz de chat que permita interactuar con el personaje como si tuviera conciencia.
- Almacenar y mostrar el historial de decisiones y evolución del personaje.

---

## 🔧 3. Tecnologías y Stack

| Componente        | Herramienta                     |
|-------------------|----------------------------------|
| Backend           | Python (Flask)                  |
| Base de datos     | SQLite                          |
| Frontend          | HTML + CSS + JavaScript (Vanilla o Vue.js) |
| Chat AI           | OpenAI API (`gpt-3.5-turbo`) o lógica local |
| Almacenamiento    | Archivos JSON / SQLite          |

---

## 🧱 4. Arquitectura General

```mermaid
graph TD
    A[Frontend (HTML/JS)] --> B[Flask Backend]
    B --> C[SQLite DB]
    B --> D[AI Engine / Logic]

📂 5. Estructura de Archivos
/echo_sheet/
├── app.py                 # Servidor Flask
├── /templates/            # HTMLs
│   ├── index.html
│   └── character.html
├── /static/
│   ├── styles.css
│   └── script.js
├── /data/                 # Archivos JSON (clases, hechizos, razas)
├── models.py              # Clases de datos
├── db.sqlite              # Base de datos
└── utils/
    ├── autofill.py        # Lógica de rellenado
    ├── recommender.py     # Sugerencias de habilidades
    └── chat_engine.py     # Chat con el personaje

🧙‍♂️ 6. Modelos de Datos
class Character:
    id: int
    name: str
    race: str
    char_class: str
    level: int
    background: str
    attributes: dict[str, int]  # STR, DEX, etc.
    skills: list[str]
    feats: list[str]
    spells: list[str]
    personality_traits: str
    history_log: list[str]
    chat_history: list[dict[str, str]]

⚙️ 7. Módulos Clave
a) Rellenado Automático (autofill.py)
Basado en clase/raza/background

Carga datos desde SRD o JSON local

Genera atributos sugeridos

b) Recomendador de Mejoras (recommender.py)
Sugiere subclases, hechizos, habilidades y mejoras según nivel y clase

Opción de mostrar una breve justificación

c) Chat Interactivo (chat_engine.py)
Simula diálogo con el personaje

Modelo simple basado en templates o con API de IA (GPT)

Incluye personalidad y eventos del personaje como contexto

🎨 8. Diseño de Interfaz
a) Pantalla Principal
Botón "Crear personaje"

Lista de personajes

Acceso rápido a ficha/chat

b) Editor de Personaje
Inputs básicos (nombre, clase, nivel)

Botón "Autocompletar"

Vista previa de la hoja

c) Vista de Ficha
Atributos, habilidades, hechizos, inventario

Botón “hablar con tu personaje”

d) Diario / Chat
Estilo chatbot

Preguntas sugeridas:

“¿Qué aprendiste hoy?”

“¿Qué opinás de nuestra última aventura?”

🔐 9. Aspectos Técnicos Avanzables (futuros)
Autenticación y sesiones de usuario

Exportación a PDF o integración con Roll20

WebSockets para modo en tiempo real

Modo campaña multijugador

✅ 10. MVP (mínimo viable)
Crear personaje (formulario básico)

Rellenado automático inicial

Vista de hoja con recomendaciones simples

Chat simulado (sin IA) basado en historial
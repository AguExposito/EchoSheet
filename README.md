# 🎲 EchoSheet - Intelligent Character Sheets for D&D

A modern web application for creating and managing Dungeons & Dragons 5e characters with integrated artificial intelligence.

## ✨ Features

- **🤖 Auto-Fill**: Generates attributes, skills and spells automatically based on class and race
- **💡 Intelligent Recommendations**: Receive suggestions for improvements, spells and optimized skills
- **💬 Interactive Chat**: Chat with your character as if they had their own consciousness
- **🎨 Modern Interface**: Attractive design with D&D theme
- **📱 Responsive**: Works perfectly on mobile and desktop devices

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd DnDCharacterCodex
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🎮 How to Use

### Create a Character
1. Go to the main page and click "Create New Character"
2. Complete the basic information (name, race, class, level)
3. Click "Auto-Fill" to generate attributes and skills automatically
4. Review the preview and click "Create Character"

### View Character Sheet
- Access the character list on the main page
- Click "View Sheet" to see all details
- Review intelligent recommendations in the sidebar

### Chat with your Character
- From the character sheet, click "Chat with [Name]"
- Use suggested questions or write your own questions
- The character will respond based on their class, race and personality

## 🏗️ Architecture

```
DnDCharacterCodex/
├── app.py                 # Main Flask server
├── models.py              # Character data model
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── AppDesignDocument.md  # Design document
├── templates/            # HTML templates
│   ├── index.html       # Main page
│   ├── create.html      # Character creation
│   ├── character.html   # Character sheet view
│   └── chat.html        # Interactive chat
├── static/              # Static files
│   ├── styles.css       # CSS styles
│   └── script.js        # JavaScript
├── utils/               # Utility modules
│   ├── autofill.py     # Character auto-fill
│   ├── recommender.py  # Recommendation system
│   └── chat_engine.py  # Chat engine
└── data/               # Game data (future)
```

## 🎯 MVP Features

### ✅ Implemented
- [x] Character creation with basic data
- [x] Automatic auto-fill of attributes and skills
- [x] Complete character sheet view with attributes, skills and spells
- [x] Intelligent recommendation system
- [x] Interactive chat with class-based personality
- [x] Modern and responsive interface
- [x] SQLite database for persistence
- [x] Character deletion with confirmation
- [x] Legal compliance with SRD (System Reference Document)

### 🔮 Future Improvements
- [ ] User authentication
- [ ] PDF export
- [ ] D&D API integration
- [ ] Modo campaña multijugador
- [ ] WebSockets para chat en tiempo real
- [ ] Más razas, clases y subclases
- [ ] Sistema de inventario
- [ ] Historial de aventuras

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Diseño**: CSS Grid, Flexbox, Gradientes
- **Fuentes**: Google Fonts (Cinzel, Crimson Text)

## 📝 Clases y Razas Soportadas (SRD Only)

### Razas
- Humano, Elfo, Enano, Mediano, Dracónido, Tiefling, Semielfo, Semiorco, Gnomo

### Clases
- Guerrero, Mago, Clérigo, Pícaro, Explorador, Paladín, Bardo, Hechicero, Brujo, Monje, Druida, Bárbaro

### Trasfondos
- Acólito, Criminal, Héroe del Pueblo, Noble, Sabio, Soldado

### ⚖️ Cumplimiento Legal
Esta aplicación utiliza únicamente contenido del **System Reference Document (SRD)** de D&D 5e, que está disponible bajo la licencia Open Game License. No se incluye contenido propietario de Wizards of the Coast para evitar problemas legales.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Wizards of the Coast por Dungeons & Dragons
- La comunidad de D&D por la inspiración
- Los desarrolladores de Flask y las librerías utilizadas

---

**¡Que tus aventuras sean épicas! 🐉⚔️** 
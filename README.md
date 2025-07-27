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
   cd EchoSheet
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

## 🧪 Testing

### Run Tests Locally
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_app.py -v
```

### Continuous Integration
This project uses GitHub Actions for automated testing and deployment:

- **CI Pipeline**: Runs on every push and pull request
- **Test Matrix**: Tests against Python 3.10 and 3.11
- **Coverage Reports**: Uploads coverage to Codecov
- **Auto Deployment**: Deploys to Render when tests pass on main branch

## 🚀 Deployment

### GitHub Actions Setup

1. **Fork/Clone the repository**

2. **Set up Render Secrets** (for auto-deployment):
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `RENDER_SERVICE_ID`: Your Render service ID
     - `RENDER_API_KEY`: Your Render API key

3. **Get Render Credentials**:
   - Service ID: Go to your Render dashboard → Service → Settings → General → Service ID
   - API Key: Go to Account Settings → API Keys → Create new API key

4. **Push to main branch**:
   - The CI will run automatically
   - If tests pass, it will deploy to Render

### Manual Deployment to Render

1. Connect your GitHub repository to Render
2. Configure the service with:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3.11.7

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
EchoSheet/
├── app.py                 # Main Flask server
├── models.py              # Character data model
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── README.md             # This file
├── AppDesignDocument.md  # Design document
├── .github/workflows/    # GitHub Actions
│   ├── ci.yml           # Continuous Integration
│   └── deploy-render.yml# Deployment to Render
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_app.py     # Application tests
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
│   ├── chat_engine.py  # Chat engine
│   └── spell_manager.py# Spell management
└── data/               # Game data
    └── spells.json     # Spell database
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
- [x] Automated testing with pytest
- [x] Continuous Integration with GitHub Actions
- [x] Automated deployment to Render

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
- **Testing**: pytest, pytest-cov
- **CI/CD**: GitHub Actions
- **Deployment**: Render

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

### Development Workflow
1. **Create a feature branch**: `git checkout -b feature/new-feature`
2. **Make changes and test locally**: `pytest`
3. **Commit changes**: `git commit -m "Add new feature"`
4. **Push and create PR**: GitHub Actions will run tests automatically
5. **Merge when tests pass**: Auto-deployment will trigger

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Wizards of the Coast por Dungeons & Dragons
- La comunidad de D&D por la inspiración
- Los desarrolladores de Flask y las librerías utilizadas

---

**¡Que tus aventuras sean épicas! 🐉⚔️** 
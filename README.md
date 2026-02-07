# Mail2PDF NextGen - README

**Convertisseur Email vers PDF Moderne, Robuste et Production-Ready**

**Version:** 2.0.0  
**License:** MIT  
**Auteur:** Ville de Fontaine 38600, France  
**Source Originale:** https://gitlab.villejuif.fr/depots-public/mail2pdf

---

## 📋 Table des Matières

- [Aperçu](#aperçu)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Support](#support)
- [License](#license)

---

## 🎯 Aperçu

**Mail2PDF NextGen** est une application production-ready pour convertir des emails de plusieurs formats (EML, MSG, MBOX, Thunderbird, ZIP) en documents PDF professionnels.

### Points Forts

✅ **Multi-Format Support:** EML, MSG, Outlook, Thunderbird, ZIP  
✅ **Gestion Encodage:** 6 niveaux de fallback (UTF-8, ISO-8859-1, Windows-1252, etc.)  
✅ **3 Interfaces:** CLI, Web (Flask), Docker  
✅ **Production-Ready:** Tests, validation, documentation complète  
✅ **Fontaine Branding:** Couleurs et styling cohérents  
✅ **Robuste:** Gestion erreurs exhaustive, logging structuré  

---

## 💻 Installation

### Option 1: Installation avec pip

```bash
# Cloner le dépôt
git clone https://github.com/Alex7209UwU/mail2pdf-nextgen.git
cd mail2pdf-nextgen

# Installer les dépendances
pip install -r requirements.txt

# Ou installer comme package
pip install .
```

### Option 2: Installation Docker

```bash
git clone https://github.com/Alex7209UwU/mail2pdf-nextgen.git
cd mail2pdf-nextgen

# Démarrer avec docker-compose
docker-compose up -d

# Accéder à l'interface
# http://localhost:5000
```

### Option 3: Installation Développeur

```bash
git clone https://github.com/Alex7209UwU/mail2pdf-nextgen.git
cd mail2pdf-nextgen

# Créer virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Lancer setup wizard
python quickstart.py
```

### Prérequis

- **Python:** 3.8+
- **Système:** Linux, macOS, Windows
- **Dépendances:** Voir `requirements.txt`

### Dépendances Clés

```
extract-msg>=0.41.1          # Parsing MSG (Outlook)
weasyprint>=60.0             # Génération PDF
chardet>=5.0.0               # Détection encodage
Flask>=2.0.0                 # Interface web
Pillow>=9.0.0                # Gestion images
```

---

## 🚀 Utilisation

### Interface CLI (Ligne de Commande)

```bash
# Conversion simple
python main.py -i email.eml -o ./pdfs

# Répertoire récursif avec logs détaillés
python main.py -i ./emails -o ./pdfs -r -v

# Validation sans conversion
python main.py -i email.msg --validate

# Configuration personnalisée
python main.py -i test.mbox -o ./out --config custom.py
```

**Options CLI:**
```
-i, --input     Fichier/dossier entrée (requis)
-o, --output    Dossier sortie (défaut: ./output)
-r, --recursive Scan récursif
-v, --verbose   Logs détaillés
--config        Fichier config personnalisé
--validate      Validation sans conversion
```

### Interface Web (Flask)

```bash
# Démarrer serveur
python app.py

# Accéder via navigateur
# http://localhost:5000
```

**Fonctionnalités Web:**
- Upload drag-and-drop
- Conversion multi-fichiers
- Téléchargement ZIP
- Status en temps réel

### Docker Deployment

```bash
# Démarrer le container
docker-compose up -d

# Arrêter
docker-compose down

# Logs
docker-compose logs -f mail2pdf
```

**Volumes:**
```
./data/input  → /app/data/input   (emails à convertir)
./data/output → /app/data/output  (PDFs générés)
```

### Module Python

```python
from main import EmailConverter

# Créer converter
converter = EmailConverter()

# Conversion simple
pdf_path = converter.convert_email('email.eml', 'output/')

# Conversion répertoire
files = converter.convert_directory('emails/', recursive=True)

# Validation
result = converter.validate('email.eml')
print(result)  # {'file': '...', 'format': 'eml', 'parseable': True, ...}
```

---

## ✨ Fonctionnalités

### Formats Supportés

| Format | Module | Type | Support |
|--------|--------|------|---------|
| EML | RFC 2822 | Text | ✅ Full |
| MSG | Outlook | Binary | ✅ Full |
| MBOX | Thunderbird | Text | ✅ Full |
| ZIP | Archive | Binary | ✅ Full |
| MIME | Multi-part | Text | ✅ Full |

### Capacités Avancées

✨ **Parsing Robuste**
- Détection automatique du format
- Support complet RFC 2822
- Handling multipart messages
- Extraction pièces jointes

✨ **Encodage Intelligent**
- 6 niveaux de fallback
- Détection vis-à-vis chardet
- Hints depuis headers
- Replacement chars si nécessaire

✨ **PDF Professionnel**
- WeasyPrint (primary) + ReportLab (fallback)
- CSS personnalisé
- Branding Ville de Fontaine
- Support HTML/plain text

✨ **Interfaces Modernes**
- CLI avec argparse
- Web Flask avec upload
- API RESTful
- Docker ready

### Gestion Erreurs

🛡️ **Robustesse Maximale**
- Try-catch exhaustifs
- Encoding fallbacks intelligents
- PDF generation fallback
- Logging structuré
- Validation pré-traitement

---

## 🏗️ Architecture

### Structure Fichiers

```
mail2pdf-nextgen/
├── main.py                    # Core engine (EmailConverter + parsers)
├── app.py                     # Flask web interface
├── config.py                  # Configuration centralisée
├── utils.py                   # Utilities (file, email, text, validation)
├── examples.py                # Usage examples
├── validate.py                # Test suite
├── setup.py                   # Package setup
├── quickstart.py              # Interactive setup
├── requirements.txt           # Dependencies
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Orchestration
├── templates/
│   ├── index.html            # Upload UI
│   ├── about.html            # Info projet
│   └── documentation.html    # API docs
├── data/
│   ├── input/               # Email files
│   └── output/              # Generated PDFs
└── docs/
    ├── README.md
    ├── CHANGELOG.md
    ├── FULL_DOCUMENTATION.md
    ├── DEPLOYMENT_*.md
    └── GITHUB_*.md
```

### Classes Principales

**EmailConverter** - Orchestration principale  
**EMLParser** - Parsing RFC 2822  
**MSGParser** - Parsing Outlook  
**MBOXParser** - Parsing Thunderbird  
**EncodingManager** - Gestion 6-niveaux encoding  
**PDFGenerator** - Génération PDF dual-engine  
**EmailTypeDetector** - Détection format automatique  
**EmailMessage** - Classe données email  

Pour plus de détails: Voir [FULL_DOCUMENTATION.md](FULL_DOCUMENTATION.md)

---

## 📚 Documentation

### Guides Disponibles

| Document | Contenu |
|----------|---------|
| [README.md](README.md) | Ce fichier (aperçu + quick start) |
| [CHANGELOG.md](CHANGELOG.md) | Historique versions v2.0.0 |
| [FULL_DOCUMENTATION.md](FULL_DOCUMENTATION.md) | Architecture ~ algorithmes détaillés |
| [DEPLOYMENT_GITHUB.md](DEPLOYMENT_GITHUB.md) | CI/CD GitHub Actions |
| [DEPLOYMENT_DOCKER.md](DEPLOYMENT_DOCKER.md) | Docker deployment guide |
| [DEPLOYMENT_SERVER.md](DEPLOYMENT_SERVER.md) | Server deployment (Linux/Windows/macOS) |
| [GITHUB_QUICKSTART.md](GITHUB_QUICKSTART.md) | 5-min quick start |
| [GITHUB_SETUP_STEPS.md](GITHUB_SETUP_STEPS.md) | Detailed step-by-step |
| [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md) | Complete GitHub setup |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Completion summary |
| [VALIDATION_REPORT.md](VALIDATION_REPORT.md) | Test results |

### Documentation Web

Docs interactives disponibles dans l'application:

- `/about` - À propos du projet
- `/documentation` - API docs avec tabs (Web/CLI/Docker/Python)

---

## 🧪 Tests et Validation

### Lancer les Tests

```bash
# Setup automatique (valide + installe)
python quickstart.py

# Tests complets
python validate.py

# Exemples d'utilisation
python examples.py
```

### Catégories de Validation

1. **File Detection** - Détection format automatique
2. **Encoding Handling** - Gestion 6-niveaux encoding
3. **PDF Structure** - Génération PDF valide
4. **Attachment Extraction** - Handling pièces jointes
5. **HTML Rendering** - Rendu CSS → PDF
6. **CLI Interface** - Cmdline arguments
7. **Web Interface** - Routes Flask
8. **Docker Container** - Image + docker-compose

---

## 🎨 Configuration

### Config Centralisée (config.py)

```python
# PDF Configuration
PDF_CONFIG = {
    'page_size': 'A4',
    'margins': {'top': '20mm', ...}
}

# Branding Colors
HTML_STYLE = {
    'primary_color': '#0088CC',      # Fontaine blue
    'secondary_color': '#00AA66',    # Green
    'accent_color': '#FFD700'        # Gold
}

# Encoding Fallback Order
ENCODING_CONFIG = {
    'fallback_order': [
        'utf-8', 'iso-8859-1', 'windows-1252',
        'utf-16', 'ascii', 'utf-8'
    ]
}
```

### Custom Configuration

```python
# Créer config.custom.py
CUSTOM_CONFIG = {...}

# Utiliser en CLI
python main.py -i email.eml --config config.custom.py
```

---

## 🔒 Sécurité

### Bonnes Pratiques Implémentées

✅ No hardcoded credentials  
✅ `secure_filename()` pour uploads  
✅ File size validation (100MB max)  
✅ Input sanitization  
✅ Auto cleanup fichiers anciens  
✅ HTTPS ready (config provided)  
✅ Non-root user dans Docker  
✅ Error messages sans stack trace  

---

## 🚨 Troubleshooting

### Problème: WeasyPrint Error

**Solution:**
```bash
# Install system dependencies
Ubuntu/Debian: sudo apt-get install libcairo2 libpango-1.0-0 libpangoft2-1.0-0
macOS: brew install cairo pango
Windows: Use pre-built wheels

# Ou utiliser Docker (embeds all deps)
docker-compose up -d
```

### Problème: MSG Parsing Error

**Solution:**
```bash
# Install extract-msg
pip install extract-msg>=0.41.1

# Vérifier installation
python -c "import extract_msg; print('OK')"
```

### Problème: Encoding Issues

**Solution:**
```bash
# Utiliser verbose mode
python main.py -i email.eml -v

# Voir logs détaillés de détection encoding
# Vérifier fallback dans config.py
```

### Problème: Docker Port En Utilisation

**Solution:**
```bash
# Changer port dans docker-compose.yml
ports:
  - "5001:5000"  # Changé de 5000 à 5001

# Ou tuer le processus existant
lsof -i :5000
kill -9 <PID>
```

---

## 📊 Performance Metrics

- **Code:** 3000+ lines of Python
- **Classes:** 9+ main classes
- **Test Coverage:** 8 validation categories
- **Docs:** 11+ comprehensive guides
- **Formats:** 5 email formats supported
- **Encodings:** 6-level fallback chain
- **Interfaces:** 3 (CLI, Web, Docker)

---

## 🤝 Contribution

### Guidelines

1. Fork le dépôt
2. Créer feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push: `git push origin feature/my-feature`
5. Submit pull request

### Areas to Contribute

- 📦 Support additional formats (EDB, PST)
- 🎨 Template customization
- 🌍 Localization (i18n)
- 🧪 Additional tests
- 📚 Documentation improvements

---

## 📝 License

MIT License - Gratuit pour usage personnel et commercial

```
Copyright (c) 2024 Ville de Fontaine 38600

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

Voir [LICENSE](LICENSE) pour texte complet.

---

## 🙏 Attribution

**Source Originale:** https://gitlab.villejuif.fr/depots-public/mail2pdf  
**Crédit:** Nous remercions les développeurs originaux de Villejuif

---

## 📞 Support et Contact

### Resources

- 📚 [Documentation Complète](FULL_DOCUMENTATION.md)
- 🐛 [Reporting Issues](https://github.com/Alex7209UwU/mail2pdf-nextgen/issues)
- 💬 [Discussions](https://github.com/Alex7209UwU/mail2pdf-nextgen/discussions)
- 📧 Email: alexis.giroudspro@outlook.fr

### Liens Importants

- GitHub: https://github.com/Alex7209UwU/mail2pdf-nextgen
- GitLab (Original): https://gitlab.villejuif.fr/depots-public/mail2pdf
- PyPI: https://pypi.org/project/mail2pdf-nextgen (future)
- Docker Hub: https://hub.docker.com/r/Alex7209UwU/mail2pdf-nextgen (future)

---

## 🎉 Conclusion

Mail2PDF NextGen est une solution robuste, production-ready pour convertir emails en PDFs.

Avec support multi-format, interfaces variées, et documentation complète, c'est l'outil idéal pour:

✨ **Archivage d'emails** - Convert important emails to PDF  
✨ **Batch Processing** - Convert thousands of emails automatically  
✨ **Integration** - Use as Python module in your apps  
✨ **Deployment** - Run on servers, Docker, or cloud  

**Happy Converting!** 📧→📄

---

**Mail2PDF NextGen v2.0.0**
Ville de Fontaine 38600, France
MIT License

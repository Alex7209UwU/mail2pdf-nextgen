# Mail2PDF NextGen - Documentation Complète

**Version:** 2.0.0  
**Licence:** MIT  
**Auteur:** Ville de Fontaine 38600, France  
**Source Originale:** https://gitlab.villejuif.fr/depots-public/mail2pdf

---

## Table des Matières

1. [Architecture](#architecture)
2. [Classes Principales](#classes-principales)
3. [Algorithmes Clés](#algorithmes-clés)
4. [Flux de Données](#flux-de-données)
5. [API Détaillée](#api-détaillée)
6. [Cas d'Utilisation](#cas-dutilisation)
7. [Optimisations](#optimisations)
8. [Limitations Connues](#limitations-connues)

---

## Architecture

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────┐
│                  Mail2PDF NextGen                       │
├─────────────────────────────────────────────────────────┤
│  Interfaces                                             │
│  ├─ Web (Flask) → /api/upload, /api/download           │
│  ├─ CLI (argparse) → -i, -o, -r, --validate            │
│  └─ Python API → EmailConverter class                  │
├─────────────────────────────────────────────────────────┤
│  Core Engine (main.py)                                  │
│  ├─ EmailTypeDetector → Format detection               │
│  ├─ EMLParser, MSGParser, MBOXParser                   │
│  ├─ EncodingManager → 6-level fallback                 │
│  ├─ PDFGenerator → WeasyPrint + fallback               │
│  └─ EmailConverter → Orchestration                     │
├─────────────────────────────────────────────────────────┤
│  Configuration (config.py)                             │
│  ├─ PDF_CONFIG, HTML_STYLE, EMAIL_CONFIG              │
│  ├─ ENCODING_CONFIG, PERFORMANCE_CONFIG               │
│  └─ VALIDATION_CONFIG, LOGGING_CONFIG                 │
├─────────────────────────────────────────────────────────┤
│  Utilities (utils.py)                                  │
│  ├─ File utilities, Email utilities                    │
│  ├─ Text/HTML sanitization                            │
│  └─ Validation helpers                                │
├─────────────────────────────────────────────────────────┤
│  Storage                                               │
│  ├─ data/input/ → Email files                         │
│  ├─ data/output/ → Generated PDFs                     │
│  └─ data/sessions/ → Conversion sessions              │
└─────────────────────────────────────────────────────────┘
```

### Diagramme de Flux

```
Input Email File
    ↓
EmailTypeDetector.detect_format()
    ↓
Parser Selection (EML/MSG/MBOX)
    ↓
Email Parsing → EmailMessage object
    ↓
EncodingManager.detect_and_decode()
    ↓
PDFGenerator.create_html()
    ↓
WeasyPrint.write_pdf() [or fallback]
    ↓
Output PDF File
```

---

## Classes Principales

### 1. EmailConverter

Classe orchestratrice principale pour la conversion d'emails.

```python
class EmailConverter:
    def __init__(self, config: Dict = None)
    def convert_email(self, input_path: str, output_dir: str) -> Optional[str]
    def convert_directory(self, input_dir: str, output_dir: str, recursive: bool) -> List[str]
    def validate(self, input_path: str) -> Dict[str, Any]
```

**Responsabilités:**
- Orchestration du flux de conversion
- Gestion des erreurs
- Logging structuré

### 2. EmailTypeDetector

Détecte automatiquement le format d'email.

```python
class EmailTypeDetector:
    @staticmethod
    def detect_format(file_path: Path) -> str
```

**Logique:**
1. Vérifier l'extension (.eml, .msg, .mbox, .zip)
2. Si non trouvée, analyser le contenu binaire
3. Chercher les signatures (PK pour ZIP, D0CF pour MSG)
4. Revenir à EML par défaut

**Formats Supportés:**
- `eml` - RFC 2822 standard
- `msg` - Outlook binary format
- `mbox` - Thunderbird/Unix format
- `zip` - Archive d'emails
- `unknown` - Fallback EML

### 3. EMLParser

Parse les emails au format RFC 2822.

```python
class EMLParser:
    @staticmethod
    def parse(file_path: Path) -> EmailMessage
    @staticmethod
    def _extract_message(msg: email.message.Message) -> EmailMessage
```

**Processus:**
1. Lire le fichier en binaire
2. Utiliser BytesParser pour RFC 2822 compliance
3. Extraire headers (Subject, From, To, Date, etc.)
4. Détecter multipart (text/plain vs text/html)
5. Gérer les pièces jointes
6. Retourner EmailMessage

### 4. MSGParser

Parse les fichiers Outlook MSG.

```python
class MSGParser:
    @staticmethod
    def parse(file_path: Path) -> EmailMessage
```

**Dépendances:**
- `extract-msg` library (optional)

**Note:** Jetable la limitation si `extract-msg` n'est pas disponible

### 5. MBOXParser

Parse le format MBOX (Thunderbird, Unix).

```python
class MBOXParser:
    @staticmethod
    def parse(file_path: Path) -> List[EmailMessage]
```

**Format MBOX:**
```
From sender@example.com date
...message content...
From sender2@example.com date
...next message...
```

**Parsage:**
1. Lire le fichier entier
2. Diviser par `\nFrom `
3. Parser chaque entrée comme RFC 2822
4. Retourner liste d'EmailMessages

### 6. EncodingManager

Gère l'encodage robuste avec fallback 6-niveaux.

```python
class EncodingManager:
    FALLBACK_ENCODINGS = [
        'utf-8', 'iso-8859-1', 'windows-1252',
        'utf-16', 'ascii', 'utf-8'  # Final avec replacement
    ]
    
    @classmethod
    def detect_and_decode(cls, data: bytes, hint_encoding: str = None) -> str
```

**Algorithme:**
1. Si hint_encoding fourni → essayer d'abord
2. Utiliser chardet pour détection statistique
3. Fallback chaîne: UTF-8 → ISO-8859-1 → … → UTF-8 (replacement)
4. Retourner string valide ou avec replacement chars

**Rationale:**
- Emails peuvent avoir encodages corrompus
- Headers contiennent parfois hint d'encodage
- Fallback intelligent récupère maximum de data

### 7. PDFGenerator

Génère PDFs avec WeasyPrint et fallback.

```python
class PDFGenerator:
    @staticmethod
    def generate(email_msg: EmailMessage, output_path: Path) -> bool
    @staticmethod
    def _create_html(email_msg: EmailMessage) -> str
    @staticmethod
    def _generate_text_pdf(html_content: str, output_path: Path) -> None
```

**Dual-Engine:**
- **Primary:** WeasyPrint (CSS → PDF)
- **Fallback:** ReportLab (text-based)

**HTML Template:**
- Header avec metadata (From, To, CC, Date)
- Body avec style CSS inline
- Footer avec attribution
- Support multipart (HTML ou plain text)

### 8. EmailMessage

Classe données pour message email.

```python
@dataclass
class EmailMessage:
    subject: str
    sender: str
    recipients: List[str]
    cc: List[str]
    bcc: List[str]
    date: str
    content_type: str
    body: str
    html_body: Optional[str] = None
    attachments: List[Dict[str, Any]] = None
    headers: Dict[str, str] = None
```

**Champs:**
- `subject` - Sujet du message
- `sender` - Adresse expéditeur
- `recipients` - Liste destinataires To:
- `cc`, `bcc` - Copies
- `date` - Date d'envoi (ISO format)
- `content_type` - text/plain ou text/html
- `body` - Contenu principal
- `html_body` - Version HTML (si disponible)
- `attachments` - Metadata pièces jointes
- `headers` - Tous les headers

### 9. LoggingConfig

Configuration structurée du logging.

```python
class LoggingConfig:
    @staticmethod
    def setup(verbose: bool = False) -> logging.Logger
```

**Niveaux:**
- `INFO` - Mode normal
- `DEBUG` - Mode verbose (-v, --verbose)

---

## Algorithmes Clés

### Détection Format Email

```
INPUT: file_path (Path)
OUTPUT: format (str)

1. extension = file_path.suffix.lower()
2. IF extension IN ['.eml', '.msg', '.mbox', '.zip']:
       RETURN extension[1:]
3. READ first 512 bytes
4. IF header starts with b'PK\x03\x04':
       RETURN 'zip'
5. IF header starts with b'\xd0\xcf\x11\xe0':
       RETURN 'msg'
6. DECODE header to text
7. IF 'From:' or 'Return-Path:' in text:
       RETURN 'eml'
8. RETURN 'eml'  # Default fallback
```

### Détection Encoding

```
INPUT: data (bytes), hint_encoding (str or None)
OUTPUT: decoded_string (str)

1. IF hint_encoding:
       TRY data.decode(hint_encoding)
       IF success: RETURN decoded_string
       ELSE: continue to step 2

2. TRY chardet.detect(data):
       IF confidence > 0.7:
           TRY decode with detected encoding
           IF success: RETURN decoded_string

3. FALLBACK LOOP:
   FOR encoding IN ['utf-8', 'iso-8859-1', 'windows-1252', 'utf-16', 'ascii']:
       TRY data.decode(encoding)
       IF success: RETURN decoded_string

4. FINAL: RETURN data.decode('utf-8', errors='replace')
```

### Parsing MBOX

```
INPUT: mbox_file (Path)
OUTPUT: messages (List[EmailMessage])

1. READ entire file as bytes
2. DETECT encoding (EncodingManager)
3. DECODE to text
4. SPLIT by '\nFrom '
5. FOR each entry:
       A. PREFIX with 'From ' if needed
       B. PARSE as RFC 2822 (email.parser)
       C. EXTRACT EmailMessage using EMLParser
       D. APPEND to results
6. RETURN results list
```

### Génération PDF

```
INPUT: email_msg (EmailMessage), output_path (Path)
OUTPUT: success (bool)

1. CREATE HTML from email_msg:
   A. Build header table (From, To, CC, Date, etc.)
   B. Insert body (HTML or wrapped plain text)
   C. Apply Fontaine branding colors
   D. Add footer avec attribution

2. TRY WeasyPrint:
       HTML(string=html_content).write_pdf(output_file)
       IF success: RETURN True

3. EXCEPT WeasyPrint error:
       TRY ReportLab fallback:
           A. EXTRACT text from HTML
           B. CREATE canvas
           C. DRAW text line by line
           D. SAVE as PDF
       IF success: RETURN True

4. RETURN False if all fail
```

---

## Flux de Données

### CLI Flow

```
$ python main.py -i emails/ -o pdfs/ -r -v

1. Parse arguments
2. Setup logging (verbose=True)
3. Create EmailConverter()
4. IF input is directory:
       convert_directory(path, recursive=True)
   ELSE:
       convert_email(path)
5. Return results
6. Exit with status code
```

### Web Flow

```
POST /api/upload
1. Validate file upload
2. Create session ID (UUID)
3. Save files to disk (session_input_dir)
4. FOR each file:
       A. Validate extension
       B. Convert to PDF
       C. Record result (success/error)
5. Save session status to JSON
6. Return JSON response with results

GET /api/download/{session_id}
1. Find all PDFs in session_output_dir
2. Create ZIP archive
3. Return as attachment

GET /api/status/{session_id}
1. Load session status JSON
2. Return JSON response
```

### Docker Flow

```
docker-compose up -d

1. Build image from Dockerfile
2. Create container
3. Mount volumes (input/, output/)
4. Start Flask app
5. Listen on 0.0.0.0:5000
6. Health check every 30s
```

---

## API Détaillée

### EmailConverter.convert_email()

**Signature:**
```python
def convert_email(
    self,
    input_path: str,
    output_dir: str = './output'
) -> Optional[str]
```

**Paramètres:**
- `input_path` (str): Chemin vers fichier email
- `output_dir` (str): Répertoire sortie

**Retour:**
- `str`: Chemin du PDF généré
- `None`: Erreur conversion

**Exceptions:**
- `FileNotFoundError`: input_path n'existe pas
- `ValueError`: Format non reconnu
- `IOError`: Erreur lecture/écriture

**Exemple:**
```python
converter = EmailConverter()
pdf = converter.convert_email('email.eml', 'output/')
# Returns: 'output/email.pdf'
```

### EmailConverter.convert_directory()

**Signature:**
```python
def convert_directory(
    self,
    input_dir: str,
    output_dir: str = './output',
    recursive: bool = False
) -> List[str]
```

**Paramètres:**
- `input_dir` (str): Chemin répertoire
- `output_dir` (str): Répertoire sortie
- `recursive` (bool): Scan sous-dossiers

**Retour:**
- `List[str]`: Chemins PDFs générés

**Exemple:**
```python
files = converter.convert_directory(
    'emails/',
    'output/',
    recursive=True
)
# Returns: ['output/email1.pdf', 'output/email2.pdf', ...]
```

### EmailConverter.validate()

**Signature:**
```python
def validate(self, input_path: str) -> Dict[str, Any]
```

**Retour:**
```python
{
    'file': str,
    'exists': bool,
    'format': str,  # 'eml', 'msg', 'mbox', 'zip', 'unknown'
    'size': int,    # bytes
    'parseable': bool,
    'errors': List[str]
}
```

---

## Cas d'Utilisation

### UC1: Conversion Simple

```python
from main import EmailConverter

converter = EmailConverter()
pdf = converter.convert_email('report.eml')
```

### UC2: Batch Processing

```python
files = converter.convert_directory('archive/', recursive=True)
print(f"Converted {len(files)} files")
```

### UC3: Web Upload

```
POST /api/upload
Content-Type: multipart/form-data

files: [email1.eml, email2.msg, email3.mbox]

Response:
{
    "session_id": "a1b2c3d4",
    "files_processed": 3,
    "files_success": 3,
    "results": [...]
}
```

### UC4: CLI Validation

```bash
python main.py -i folder/ --validate
```

---

## Optimisations

### Performance

1. **Encoding Detection:** Chardet utilisé pour speedup vs brute-force fallback
2. **Lazy Parsing:** Headers parsés seulement si needed
3. **Stream Processing:** PDFs générés directement sans buffer intermédiaire
4. **Batch Mode:** Traitement efficace de multiples emails

### Memory

1. **File Streaming:** Gros fichiers lus par chunks
2. **Session Cleanup:** Fichiers temp supprimés après 7 jours
3. **Resource Limits:** Docker limité à 2GB RAM

### Reliability

1. **Fallback Chains:** Encoding, PDF generation, parsing
2. **Error Handling:** Try-catch exhaustifs
3. **Validation:** Checks avant et après conversion
4. **Logging:** Traces détaillées pour debug

---

## Limitations Connues

### Technical

1. **WeasyPrint Limitations:**
   - Pas support CSS3 avancé
   - Conversion images losse possible

2. **MSG Parsing:**
   - Requiert `extract-msg` (optional)
   - Pièces jointes complexes possibles

3. **ZIP Support:**
   - Seuls emails à la racine du ZIP
   - Pas support nested archives

### Encoding

1. **Caractères Corrompus:**
   - Fallback utilise replacement chars
   - Peut créer output lisible mais pas parfait

2. **Encodages Mixtes:**
   - Headers UTF-8, body ISO-8859-1
   - Fallback chaîne gère mais pas optimal

### Performance

1. **Gros Emails:**
   - WeasyPrint peut être lent (>100MB)
   - Timeout 30s configurable

2. **Beaucoup d'Attachments:**
   - Metadata seulement, pas extraction complète

---

## Configuration Avancée

### Custom Encoding Fallback

Modifier dans `config.py`:
```python
ENCODING_CONFIG = {
    'fallback_order': [
        'utf-8',
        'iso-8859-1',
        'windows-1252',
        # Add more here
    ]
}
```

### Custom PDF Styling

Modifier dans `config.py`:
```python
HTML_STYLE = {
    'primary_color': '#0088CC',  # Fontaine blue
    # Change colors, fonts, layout
}
```

### Docker Resource Limits

Modifier dans `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Increase if needed
```

---

## Version History

**v2.0.0** (2024-01-15)
- Initial production release
- Full multi-format support
- Web, CLI, Docker interfaces
- Comprehensive documentation

---

**Mail2PDF NextGen** • Licence MIT

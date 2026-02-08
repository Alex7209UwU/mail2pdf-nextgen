#!/usr/bin/env python3
"""
Mail2PDF NextGen - Flask Web Interface
Ville de Fontaine 38600, France
"""

import os
import logging
import json
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename  # type: ignore
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, flash, redirect, url_for  # type: ignore
import shutil

from main import EmailConverter, LoggingConfig  # type: ignore

from typing import Dict, Any, Optional, Union, List

# ============================================================================
# FLASK APPLICATION SETUP
# ============================================================================

app = Flask(__name__, template_folder='templates')

# Configuration
app.config['UPLOAD_FOLDER'] = Path('./data/input')
app.config['OUTPUT_FOLDER'] = Path('./data/output')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'eml', 'msg', 'mbox', 'zip'}
app.config['SESSION_FOLDER'] = Path('./data/sessions')

# Setup directories
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], 
               app.config['SESSION_FOLDER']]:
    folder.mkdir(parents=True, exist_ok=True)

# Setup logging
logger = LoggingConfig.setup(verbose=False)
app = Flask(__name__, template_folder='templates')

# Re-apply configuration after Flask init
app.config['UPLOAD_FOLDER'] = Path('./data/input')
app.config['OUTPUT_FOLDER'] = Path('./data/output')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'eml', 'msg', 'mbox', 'zip'}
app.config['SESSION_FOLDER'] = Path('./data/sessions')
app.config['CONFIG_FILE'] = Path('./data/config_dynamic.json')
app.config['LANG_FILE'] = Path('./data/languages.json')
app.config['LOGO_FOLDER'] = Path('./static/logos')
app.config['LOGO_FOLDER'].mkdir(parents=True, exist_ok=True)
app.secret_key = 'supersecretkey'  # Needed for flash messages

DEFAULT_CONFIG: Dict[str, Any] = {
    "language": "fr",
    "colors": {
        "primary": "#0088CC",
        "secondary": "#00AA66",
        "accent": "#FFD700",
        "background": "#f5f5f5",
        "text": "#333333"
    },
    "logo_path": None
}

def load_dynamic_config() -> Dict[str, Any]:
    if app.config['CONFIG_FILE'].exists():
        try:
            with open(app.config['CONFIG_FILE'], 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error decoding config file, using default.")
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_dynamic_config(config: Dict[str, Any]) -> None:
    try:
        with open(app.config['CONFIG_FILE'], 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving config file: {e}")
        raise

DEFAULT_MESSAGES: Dict[str, Dict[str, str]] = {
    "fr": {
        "title": "Mail2PDF NextGen",
        "tagline": "Convertisseur Email vers PDF",
        "upload_title": "Importer vos emails",
        "files_selected": "Fichiers sélectionnés",
        "convert_button": "Convertir en PDF",
        "results_title": "Résultats",
        "download_button": "Télécharger les PDF (ZIP)",
        "nav_about": "À Propos",
        "nav_docs": "Documentation",
        "nav_github": "GitHub",
        "nav_configure": "Configurer",
        "footer_version": "v1.0.0",
        "footer_license": "Licence MIT",
        "footer_brand": "Ville de Fontaine",
        "footer_source": "Source",
        # Fallbacks for critical keys
    },
    "en": {
        "title": "Mail2PDF NextGen",
        "tagline": "Email to PDF Converter",
        "upload_title": "Import your emails",
        "files_selected": "Selected files",
        "convert_button": "Convert to PDF",
        "results_title": "Results",
        "download_button": "Download PDFs (ZIP)",
        "nav_about": "About",
        "nav_docs": "Documentation",
        "nav_github": "GitHub",
        "nav_configure": "Configure",
        "footer_version": "v1.0.0",
        "footer_license": "MIT License",
        "footer_brand": "City of Fontaine",
        "footer_source": "Source",
    }
}

def load_languages() -> Dict[str, Dict[str, str]]:
    languages = DEFAULT_MESSAGES.copy()
    if app.config['LANG_FILE'].exists():
        try:
            with open(app.config['LANG_FILE'], 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                # Deep merge or update
                if isinstance(loaded, dict):
                    for lang, messages in loaded.items():
                        if isinstance(messages, dict):
                            if lang in languages:
                                languages[lang].update(messages) # type: ignore
                            else:
                                languages[lang] = messages # type: ignore
        except Exception as e:
            logger.error(f"Error loading languages file: {e}")
    return languages

@app.context_processor
def inject_config():
    config = load_dynamic_config()
    languages = load_languages()
    
    # Ensure selected language exists in messages
    lang = config.get('language', 'fr')
    if lang not in languages:  # type: ignore
        config['language'] = 'fr' if 'fr' in languages else 'en'
        
    return dict(config=config, text=languages)

# Initialize converter
converter = EmailConverter()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  # type: ignore


def cleanup_old_files(days: int = 7) -> None:
    """Remove files older than specified days."""
    try:
        cutoff = datetime.now() - timedelta(days=days)
        
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            for file_path in folder.rglob('*'):
                if file_path.is_file():
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff:
                        file_path.unlink()
                        logger.debug(f"Cleaned up old file: {file_path}")
    
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


def get_session_status(session_id: str) -> dict:
    """Get status for a conversion session."""
    session_file = app.config['SESSION_FOLDER'] / f"{session_id}.json"
    
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f)
    
    return {'status': 'not_found', 'files': 0}


def save_session_status(session_id: str, status: dict) -> None:
    """Save session status to file."""
    session_file = app.config['SESSION_FOLDER'] / f"{session_id}.json"
    
    with open(session_file, 'w') as f:
        json.dump(status, f)


# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve main upload page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return jsonify({'error': 'Template not found'}), 500


@app.route('/about')
def about():
    """Serve about page with project info."""
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Error rendering about: {e}")
        return jsonify({'error': 'Template not found'}), 500


@app.route('/documentation')
def documentation():
    """Serve API documentation page."""
    try:
        return render_template('documentation.html')
    except Exception as e:
        logger.error(f"Error rendering documentation: {e}")
        return jsonify({'error': 'Template not found'}), 500


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """
    Handle file uploads and convert to PDF.
    
    Returns:
        JSON with conversion results and download link
    """
    try:
        # Validate upload
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')  # type: ignore
        
        if not files or all(f.filename == '' for f in files):  # type: ignore
            return jsonify({'error': 'No files selected'}), 400
        
        # Create session
        import uuid
        session_id = str(uuid.uuid4())[:8]  # type: ignore
        
        logger.info(f"Session {session_id}: Starting upload processing")
        
        # Process files
        uploaded_files = []
        conversion_results = []
        
        # Extract options
        options = {
            'extract_attachments': request.form.get('extract_attachments') == 'true',
            'page_size': request.form.get('page_size', 'A4'),
            'orientation': request.form.get('orientation', 'portrait')
        }
        
        for file in files:
            if not allowed_file(file.filename):
                logger.warning(f"Rejected file: {file.filename}")
                continue
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            session_input_dir = app.config['UPLOAD_FOLDER'] / session_id
            session_input_dir.mkdir(exist_ok=True)
            
            file_path = session_input_dir / filename
            file.save(str(file_path))
            
            logger.info(f"Session {session_id}: File saved: {filename}")
            uploaded_files.append(filename)
            
            # Convert to PDF
            session_output_dir = app.config['OUTPUT_FOLDER'] / session_id
            session_output_dir.mkdir(exist_ok=True)
            
            try:
                pdf_path = converter.convert_email(str(file_path), str(session_output_dir), options)
                
                if pdf_path:
                    conversion_results.append({
                        'input': filename,
                        'output': Path(pdf_path).name,  # type: ignore
                        'status': 'success'
                    })
                    logger.info(f"Session {session_id}: Converted {filename}")
                else:
                    conversion_results.append({
                        'input': filename,
                        'status': 'error',
                        'error': 'PDF generation failed'
                    })
            
            except Exception as e:
                logger.error(f"Session {session_id}: Conversion error: {e}")
                conversion_results.append({
                    'input': filename,
                    'status': 'error',
                    'error': str(e)
                })
        
        # Save session status
        status = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'files_processed': len(conversion_results),
            'files_success': sum(1 for r in conversion_results if r['status'] == 'success'),
            'files_failed': sum(1 for r in conversion_results if r['status'] == 'error'),
            'results': conversion_results
        }
        
        save_session_status(session_id, status)
        
        return jsonify(status), 200
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/preview', methods=['POST'])
def preview_email():
    """
    Handle email preview requests.
    Returns:
        JSON with HTML content or error
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not allowed_file(file.filename): # type: ignore
            return jsonify({'error': 'File type not allowed'}), 400
            
        # Create temp directory for preview
        import uuid
        preview_id = str(uuid.uuid4())[:8]  # type: ignore
        preview_dir = app.config['UPLOAD_FOLDER'] / 'previews' / preview_id
        preview_dir.mkdir(parents=True, exist_ok=True)
        
        filename = secure_filename(file.filename) # type: ignore
        file_path = preview_dir / filename
        file.save(str(file_path))
        
        # Generate preview
        html_content = converter.get_preview_html(str(file_path))
        
        # Cleanup (optional, or rely on periodic cleanup)
        # Cleanup
        try:
            if preview_dir.exists():
                import shutil
                shutil.rmtree(preview_dir)
        except Exception as e:
            logger.warning(f"Preview cleanup failed: {e}")
            
        if html_content:
            return jsonify({'html': html_content})
        else:
            return jsonify({'error': 'Failed to generate preview'}), 500
            
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<session_id>')
def download_pdfs(session_id: str):
    """
    Download all PDFs from a session as ZIP.
    
    Args:
        session_id: Session identifier
        
    Returns:
        ZIP file with all converted PDFs
    """
    try:
        output_dir = app.config['OUTPUT_FOLDER'] / session_id
        
        if not output_dir.exists():
            return jsonify({'error': 'Session not found'}), 404
        
        # Find all PDFs
        pdfs: List[Path] = list(output_dir.glob('*.pdf'))
        
        if not pdfs:
            return jsonify({'error': 'No PDFs available for download'}), 404
        
        # Create ZIP
        zip_path = app.config['SESSION_FOLDER'] / f"{session_id}.zip"
        
        with zipfile.ZipFile(str(zip_path), 'w') as zf:
            for pdf in pdfs:
                zf.write(str(pdf), arcname=pdf.name)
        
        logger.info(f"Session {session_id}: Created download ZIP with {len(pdfs)} files")
        
        return send_file(
            str(zip_path),
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'mail2pdf_{session_id}.zip'
        )
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/api/status/<session_id>')
def get_status(session_id: str):
    """
    Get conversion status for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        JSON with session status and progress
    """
    try:
        status = get_session_status(session_id)
        
        if status.get('status') == 'not_found':
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify(status), 200
    
    except Exception as e:
        logger.error(f"Status error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/configure', methods=['GET', 'POST'])
def configure():
    """Handle site configuration."""
    if request.method == 'POST':
        try:
            current_config = load_dynamic_config()
            
            # Update language
            new_lang = request.form.get('language', 'fr')
            langs = load_languages()
            if new_lang in langs:
                current_config['language'] = new_lang
            else:
                current_config['language'] = 'fr'  # Fallback

            
            # Update colors
            current_config['colors'] = {
                'primary': request.form.get('color_primary', '#0088CC'),
                'secondary': request.form.get('color_secondary', '#00AA66'),
                'accent': request.form.get('color_accent', '#FFD700'),
                'background': request.form.get('color_background', '#f5f5f5'),
                'text': request.form.get('color_text', '#333333')
            }
            
            # Handle logo upload
            if 'logo' in request.files:
                file = request.files['logo']
                if file and file.filename:
                    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                        filename = secure_filename(f"logo_{int(datetime.now().timestamp())}.{file.filename.split('.')[-1]}")
                        file.save(str(app.config['LOGO_FOLDER'] / filename))
                        
                        # Remove old logo if exists
                        old_logo = current_config.get('logo_path')
                        if old_logo:
                            try:
                                old_path = Path(app.root_path) / 'static' / old_logo
                                if old_path.exists():
                                    old_path.unlink()
                            except Exception as e:
                                logger.warning(f"Failed to remove old logo: {e}")
                        
                        current_config['logo_path'] = f"logos/{filename}"
            
            save_dynamic_config(current_config)
            
            # Get success message in correct language
            langs = load_languages()
            lang = current_config.get('language', 'fr')
            if isinstance(langs, dict) and lang in langs:
                flash(langs[lang].get('config_saved', 'Configuration saved!'), 'success')
            else:
                 flash('Configuration saved!', 'success')
            
            return redirect(url_for('configure'))
            
        except Exception as e:
            logger.error(f"Configuration error: {e}")
            flash(f"Error: {e}", 'error')
            return redirect(url_for('configure'))
    
    return render_template('configure.html')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large (max 100MB)'}), 413


@app.route('/api/history')
def get_history():
    """
    Get conversion history.
    Returns:
        JSON list of past sessions
    """
    try:
        history = []
        if not app.config['SESSION_FOLDER'].exists():
            return jsonify([])
            
        for file_path in app.config['SESSION_FOLDER'].glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    history.append({
                        'session_id': data.get('session_id'),
                        'timestamp': data.get('timestamp'),
                        'files_processed': data.get('files_processed', 0),
                        'files_success': data.get('files_success', 0),
                        'files_failed': data.get('files_failed', 0),
                        'status': data.get('status', 'unknown')
                    })
            except Exception:
                continue
        
        # Sort by timestamp descending
        history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return jsonify(history)
        
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    logger.info("Mail2PDF NextGen - Flask Web Interface Starting")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Output folder: {app.config['OUTPUT_FOLDER']}")
    
    # Cleanup old files on startup
    cleanup_old_files(days=7)
    
    # Start Flask development server
    app.run(host='0.0.0.0', port=5000, debug=False)

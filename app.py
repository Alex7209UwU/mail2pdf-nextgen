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
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import shutil

from main import EmailConverter, LoggingConfig

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

# Initialize converter
converter = EmailConverter()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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
        
        files = request.files.getlist('files')
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        # Create session
        import uuid
        session_id = str(uuid.uuid4())[:8]
        
        logger.info(f"Session {session_id}: Starting upload processing")
        
        # Process files
        uploaded_files = []
        conversion_results = []
        
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
                pdf_path = converter.convert_email(str(file_path), str(session_output_dir))
                
                if pdf_path:
                    conversion_results.append({
                        'input': filename,
                        'output': Path(pdf_path).name,
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
            'results': conversion_results
        }
        
        save_session_status(session_id, status)
        
        return jsonify(status), 200
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


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
        pdfs = list(output_dir.glob('*.pdf'))
        
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


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large (max 100MB)'}), 413


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

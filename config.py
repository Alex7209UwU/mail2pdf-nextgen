#!/usr/bin/env python3
"""
Mail2PDF NextGen - Central Configuration
Ville de Fontaine 38600, France
"""

# ============================================================================
# PDF CONFIGURATION
# ============================================================================

PDF_CONFIG = {
    'page_size': 'A4',  # A4, Letter, A3, etc.
    'page_width': '210mm',
    'page_height': '297mm',
    'margins': {
        'top': '20mm',
        'right': '20mm',
        'bottom': '20mm',
        'left': '20mm'
    },
    'font_family': 'Arial, sans-serif',
    'font_size': '11pt',
    'line_height': '1.6',
    'quality': 300,  # DPI
    'compression': True
}

# ============================================================================
# HTML/CSS STYLING
# ============================================================================

HTML_STYLE = {
    'primary_color': '#0088CC',  # Ville de Fontaine blue
    'secondary_color': '#00AA66',  # Green
    'accent_color': '#FFD700',  # Gold
    'background_color': '#f5f5f5',
    'text_color': '#333333',
    'border_color': '#dddddd',
    'header_background': '#ffffff',
    'footer_background': '#f9f9f9',
    'link_color': '#0088CC',
    'code_background': '#f4f4f4',
    'warning_color': '#ff6b6b',
    'success_color': '#51cf66'
}

CSS_INLINE = """
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: %COLOR%;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
}

.email-container {
    background-color: white;
    border: 1px solid %BORDER%;
    border-radius: 5px;
    padding: 20px;
    max-width: 900px;
    margin: 0 auto;
}

.header {
    border-bottom: 3px solid %PRIMARY%;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.header-title {
    color: %PRIMARY%;
    font-size: 20px;
    font-weight: bold;
    margin: 0 0 15px 0;
    word-wrap: break-word;
}

.header-meta {
    display: grid;
    grid-template-columns: 100px 1fr;
    gap: 10px;
    font-size: 13px;
    color: #666;
}

.meta-label {
    font-weight: bold;
    color: %PRIMARY%;
}

.body {
    margin-top: 20px;
    color: %TEXT%;
}

.body p {
    margin: 10px 0;
}

.body pre {
    background-color: %CODE%;
    padding: 12px;
    border-radius: 3px;
    overflow-x: auto;
    border-left: 3px solid %SECONDARY%;
}

.body a {
    color: %LINK%;
    text-decoration: none;
}

.body a:hover {
    text-decoration: underline;
}

.signature {
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid %BORDER%;
    font-size: 12px;
    color: #999;
}

.footer {
    margin-top: 25px;
    padding-top: 15px;
    border-top: 2px solid %SECONDARY%;
    font-size: 11px;
    color: #999;
    text-align: center;
}

.attachments {
    margin-top: 15px;
    padding: 10px;
    background-color: %FOOTER%;
    border-radius: 3px;
    border-left: 3px solid %ACCENT%;
}

.attachment-item {
    margin: 5px 0;
    font-size: 12px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}

table th {
    background-color: %PRIMARY%;
    color: white;
    padding: 10px;
    text-align: left;
}

table td {
    padding: 8px 10px;
    border-bottom: 1px solid %BORDER%;
}

table tr:nth-child(even) {
    background-color: %FOOTER%;
}

blockquote {
    border-left: 3px solid %SECONDARY%;
    margin: 10px 0;
    padding-left: 15px;
    color: #666;
}

.quote-author {
    font-size: 12px;
    color: #999;
    margin-top: 5px;
}
""" % HTML_STYLE

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_CONFIG = {
    'headers_to_extract': [
        'Subject',
        'From',
        'To',
        'Cc',
        'Bcc',
        'Date',
        'Message-ID',
        'Reply-To',
        'In-Reply-To',
        'References',
        'Content-Type',
        'X-Priority',
        'Importance'
    ],
    'display_headers': {
        'Subject': 'Subject',
        'From': 'From',
        'To': 'To',
        'Cc': 'CC',
        'Bcc': 'BCC',
        'Date': 'Date',
        'Reply-To': 'Reply-To',
        'X-Priority': 'Priority'
    },
    'regex_patterns': {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'url': r'https?://[^\s<>"{}|\\^`\[\]]+'
    },
    'quote_markers': ['>>', '>', '-----Original Message-----'],
    'max_body_length': 50000,  # Characters
    'extract_attachments': True
}

# ============================================================================
# ENCODING CONFIGURATION
# ============================================================================

ENCODING_CONFIG = {
    'fallback_order': [
        'utf-8',
        'iso-8859-1',
        'windows-1252',
        'utf-16',
        'ascii',
        'utf-8'  # Final with replacement
    ],
    'replacement_char': '?',
    'use_chardet': True,
    'chardet_confidence_threshold': 0.7,
    'detect_from_content': True,
    'detect_from_headers': True
}

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

PERFORMANCE_CONFIG = {
    'weasyprint_timeout': 30,  # seconds
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'batch_size': 10,
    'thread_count': 4,
    'memory_limit': 2 * 1024 * 1024 * 1024,  # 2GB
    'cleanup_temp_files': True,
    'cleanup_interval': 86400,  # 24 hours
    'max_pdf_size': 50 * 1024 * 1024,  # 50MB
    'use_cache': False,
    'cache_size': 1000
}

# ============================================================================
# VALIDATION CONFIGURATION
# ============================================================================

VALIDATION_CONFIG = {
    'check_file_exists': True,
    'check_file_readable': True,
    'check_format_detection': True,
    'check_encoding': True,
    'check_pdf_generation': True,
    'check_output_valid': True,
    'check_file_size': True,
    'check_email_structure': True,
    'categories': [
        'file_detection',
        'encoding_handling',
        'pdf_structure',
        'attachment_extraction',
        'html_rendering',
        'cli_interface',
        'web_interface',
        'docker_container'
    ]
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'mail2pdf.log'
        }
    },
    'loggers': {
        'mail2pdf': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': False,
    'max_content_length': 100 * 1024 * 1024,  # 100MB
    'upload_folder': './data/input',
    'output_folder': './data/output',
    'allowed_extensions': ['eml', 'msg', 'mbox', 'zip'],
    'session_timeout': 3600,  # 1 hour
    'cleanup_days': 7  # Remove files older than 7 days
}

# ============================================================================
# DOCKER CONFIGURATION
# ============================================================================

DOCKER_CONFIG = {
    'image': 'mail2pdf-nextgen',
    'version': '2.0.0',
    'base_image': 'python:3.11-slim',
    'user': 'appuser',
    'uid': 1000,
    'gid': 1000,
    'volumes': {
        'input': '/app/data/input',
        'output': '/app/data/output'
    },
    'ports': {
        'web': 5000
    },
    'environment': {
        'PYTHONUNBUFFERED': '1',
        'FLASK_ENV': 'production'
    },
    'health_check': {
        'test': 'curl -f http://localhost:5000/ || exit 1',
        'interval': '30s',
        'timeout': '10s',
        'retries': 3,
        'start_period': '40s'
    },
    'memory_limit': '2g',
    'restart_policy': 'unless-stopped'
}

# ============================================================================
# APPLICATION METADATA
# ============================================================================

APP_METADATA = {
    'name': 'Mail2PDF NextGen',
    'version': '2.0.0',
    'author': 'Ville de Fontaine 38600',
    'license': 'MIT',
    'homepage': 'https://github.com/yourusername/mail2pdf-nextgen',
    'repository': 'https://gitlab.villejuif.fr/depots-public/mail2pdf',
    'description': 'Advanced Email to PDF Converter with multi-format support',
    'keywords': ['email', 'pdf', 'converter', 'eml', 'msg', 'mbox'],
    'python_requires': '>=3.8'
}

# ============================================================================
# Get full configuration dictionary
# ============================================================================

def get_config() -> dict:
    """Get complete configuration dictionary."""
    return {
        'pdf': PDF_CONFIG,
        'html': HTML_STYLE,
        'css': CSS_INLINE,
        'email': EMAIL_CONFIG,
        'encoding': ENCODING_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'validation': VALIDATION_CONFIG,
        'logging': LOGGING_CONFIG,
        'flask': FLASK_CONFIG,
        'docker': DOCKER_CONFIG,
        'metadata': APP_METADATA
    }

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_config())

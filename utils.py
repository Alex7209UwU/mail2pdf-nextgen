#!/usr/bin/env python3
"""
Mail2PDF NextGen - Utility Functions
Ville de Fontaine 38600, France
"""

import os
import sys
import re
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import hashlib
import tempfile
import json
import logging

logger = logging.getLogger('mail2pdf.utils')


# ============================================================================
# FILE UTILITIES
# ============================================================================

def get_safe_filename(filename: str, max_length: int = 255) -> str:
    """
    Create safe filename by removing unsafe characters.
    
    Args:
        filename: Original filename
        max_length: Maximum filename length
        
    Returns:
        Safe filename
    """
    # Remove invalid characters
    safe = re.sub(r'[<>:"/\\|?*]', '', filename)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'[^a-zA-Z0-9._-]', '', safe)
    
    # Limit length
    if len(safe) > max_length:
        name, ext = safe.rsplit('.', 1) if '.' in safe else (safe, '')
        safe = name[:max_length - len(ext) - 1] + '.' + ext if ext else safe[:max_length]
    
    return safe or 'file'


def get_file_hash(file_path: Path, algorithm: str = 'sha256') -> str:
    """
    Calculate file hash.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)
        
    Returns:
        Hex digest of file
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def get_file_size_human(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def find_files(directory: Path, pattern: str = '*', recursive: bool = False) -> List[Path]:
    """
    Find files in directory matching pattern.
    
    Args:
        directory: Directory to search
        pattern: File pattern (glob)
        recursive: Search subdirectories
        
    Returns:
        List of matching file paths
    """
    if not directory.is_dir():
        return []
    
    glob_method = directory.rglob if recursive else directory.glob
    return sorted([f for f in glob_method(pattern) if f.is_file()])


def ensure_directory(directory: Path) -> Path:
    """Create directory if it doesn't exist."""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def remove_directory(directory: Path) -> None:
    """Recursively remove directory and contents."""
    import shutil
    if directory.exists():
        shutil.rmtree(directory)


# ============================================================================
# EMAIL UTILITIES
# ============================================================================

def extract_email_address(email_string: str) -> Optional[str]:
    """
    Extract email address from string like "John Doe <john@example.com>".
    
    Args:
        email_string: Email string with optional name
        
    Returns:
        Email address or None
    """
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_string)
    return match.group(0) if match else None


def normalize_email_list(email_list: List[str]) -> List[str]:
    """
    Normalize and deduplicate email list.
    
    Args:
        email_list: List of email addresses (may include names)
        
    Returns:
        Sorted list of unique email addresses
    """
    emails = set()
    
    for email_str in email_list:
        email = extract_email_address(email_str.strip())
        if email:
            emails.add(email.lower())
    
    return sorted(list(emails))


def parse_email_header(header_value: str) -> List[str]:
    """
    Parse email header value (handles encoded words, multiple addresses).
    
    Args:
        header_value: Header value string
        
    Returns:
        List of parsed values
    """
    from email.header import decode_header
    
    try:
        decoded_parts = []
        
        for part, encoding in decode_header(header_value):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
            else:
                decoded_parts.append(str(part))
        
        return [''.join(decoded_parts)]
    
    except Exception as e:
        logger.warning(f"Error parsing header: {e}")
        return [header_value]


def clean_email_body(body: str, remove_signatures: bool = True, 
                    remove_quotes: bool = False) -> str:
    """
    Clean email body by removing signatures and quotes.
    
    Args:
        body: Email body text
        remove_signatures: Remove common signature patterns
        remove_quotes: Remove quoted text
        
    Returns:
        Cleaned body text
    """
    lines = body.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip signature separators
        if remove_signatures and line.strip() in ['--', '___', '===']:
            break
        
        # Skip block quotes
        if remove_quotes and line.strip().startswith(('>', '--')):
            continue
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines).strip()


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (not including suffix)
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def sanitize_html(html_content: str, allowed_tags: Optional[List[str]] = None) -> str:
    """
    Remove potentially dangerous HTML tags.
    
    Args:
        html_content: HTML content to sanitize
        allowed_tags: List of allowed tags (default: safe tags only)
        
    Returns:
        Sanitized HTML
    """
    if allowed_tags is None:
        allowed_tags = ['p', 'br', 'b', 'i', 'u', 'strong', 'em', 'a', 'ul', 'ol', 'li',
                       'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
                       'table', 'tr', 'th', 'td', 'div', 'span']
    
    # Simple regex-based tag removal (not perfect, but effective for most cases)
    dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form', 'input']
    
    for tag in dangerous_tags:
        html_content = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(f'<{tag}[^>]*>', '', html_content, flags=re.IGNORECASE)
    
    return html_content


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


# ============================================================================
# DATE/TIME UTILITIES
# ============================================================================

def parse_email_date(date_str: str) -> Optional[datetime]:
    """
    Parse email date string to datetime object.
    
    Args:
        date_str: Email date string (RFC 2822 format)
        
    Returns:
        Datetime object or None
    """
    from email.utils import parsedate_to_datetime
    
    try:
        return parsedate_to_datetime(date_str)
    except (TypeError, ValueError):
        logger.warning(f"Failed to parse date: {date_str}")
        return None


def format_date_human(date_obj: datetime) -> str:
    """
    Format datetime in human-readable format.
    
    Args:
        date_obj: Datetime object
        
    Returns:
        Formatted date string
    """
    return date_obj.strftime('%B %d, %Y at %H:%M:%S')


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def is_safe_filename(filename: str) -> bool:
    """
    Check if filename is safe (no path traversal attempts).
    
    Args:
        filename: Filename to check
        
    Returns:
        True if safe
    """
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    return True


def validate_file_size(file_path: Path, max_size: int) -> bool:
    """
    Validate file size.
    
    Args:
        file_path: Path to file
        max_size: Maximum size in bytes
        
    Returns:
        True if file is within size limit
    """
    try:
        return file_path.stat().st_size <= max_size
    except Exception:
        return False


# ============================================================================
# JSON UTILITIES
# ============================================================================

def read_json_file(file_path: Path) -> Optional[Dict]:
    """Read JSON file safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading JSON file {file_path}: {e}")
        return None


def write_json_file(file_path: Path, data: Dict, pretty: bool = True) -> bool:
    """Write JSON file safely."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2 if pretty else None)
        return True
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {e}")
        return False


# ============================================================================
# TEMPORARY FILE UTILITIES
# ============================================================================

def create_temp_dir(prefix: str = 'mail2pdf_') -> Path:
    """Create temporary directory."""
    return Path(tempfile.mkdtemp(prefix=prefix))


def create_temp_file(suffix: str = '.tmp', prefix: str = 'mail2pdf_') -> Path:
    """Create temporary file."""
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)
    return Path(path)


# ============================================================================
# SYSTEM UTILITIES
# ============================================================================

def get_system_info() -> Dict[str, str]:
    """Get system information."""
    import platform
    
    return {
        'system': platform.system(),
        'release': platform.release(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor()
    }


def check_required_module(module_name: str) -> bool:
    """Check if required module is available."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        logger.warning(f"Required module not available: {module_name}")
        return False


if __name__ == '__main__':
    # Test utilities
    print("Email validation:", is_valid_email('test@example.com'))
    print("Safe filename:", get_safe_filename('invalid/filename<>.txt'))
    print("File size human:", get_file_size_human(1024 * 1024 * 100))
    print("System info:", get_system_info())

#!/usr/bin/env python3
"""
Mail2PDF NextGen - Examples and Usage Demonstrations
Ville de Fontaine 38600, France
"""

from pathlib import Path
import logging
from main import EmailConverter, LoggingConfig

# Setup logging
logger = LoggingConfig.setup(verbose=True)


def example_1_simple_conversion():
    """Example 1: Simple email to PDF conversion."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Simple Email to PDF Conversion")
    print("=" * 80)
    
    converter = EmailConverter()
    
    # Convert single email
    pdf_path = converter.convert_email(
        input_path='data/input/test_email.eml',
        output_dir='data/output/example1'
    )
    
    if pdf_path:
        print(f"✓ Successfully converted to: {pdf_path}")
    else:
        print("✗ Conversion failed")


def example_2_directory_conversion():
    """Example 2: Convert all emails in a directory."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Directory Conversion (Recursive)")
    print("=" * 80)
    
    converter = EmailConverter()
    
    # Convert entire directory recursively
    results = converter.convert_directory(
        input_dir='data/input',
        output_dir='data/output/example2',
        recursive=True
    )
    
    print(f"✓ Converted {len(results)} files:")
    for pdf_path in results:
        print(f"  - {pdf_path}")


def example_3_email_validation():
    """Example 3: Validate emails without conversion."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Email Validation")
    print("=" * 80)
    
    converter = EmailConverter()
    
    # Validate without converting
    result = converter.validate('data/input/test_email.eml')
    
    print(f"File: {result['file']}")
    print(f"Format: {result['format']}")
    print(f"Size: {result['size']} bytes")
    print(f"Parseable: {result['parseable']}")
    
    if result['errors']:
        print("Errors:")
        for error in result['errors']:
            print(f"  - {error}")


def example_4_custom_config():
    """Example 4: Using custom configuration."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Custom Configuration")
    print("=" * 80)
    
    from config import get_config
    
    # Get and display configuration
    config = get_config()
    
    print("\nPDF Configuration:")
    print(f"  Page Size: {config['pdf']['page_size']}")
    print(f"  Margins: {config['pdf']['margins']}")
    
    print("\nBranding Colors:")
    print(f"  Primary: {config['html']['primary_color']}")
    print(f"  Secondary: {config['html']['secondary_color']}")
    print(f"  Accent: {config['html']['accent_color']}")
    
    print("\nEncoding Fallback Order:")
    for idx, enc in enumerate(config['encoding']['fallback_order'], 1):
        print(f"  {idx}. {enc}")


def example_5_email_parsing():
    """Example 5: Parse email and inspect contents."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Email Parsing and Inspection")
    print("=" * 80)
    
    from main import EMLParser
    
    # Parse EML file
    email_msg = EMLParser.parse(Path('data/input/test_email.eml'))
    
    print(f"Subject: {email_msg.subject}")
    print(f"From: {email_msg.sender}")
    print(f"To: {', '.join(email_msg.recipients)}")
    print(f"CC: {', '.join(email_msg.cc) if email_msg.cc else 'None'}")
    print(f"Date: {email_msg.date}")
    print(f"Attachments: {len(email_msg.attachments)}")
    
    print(f"\nBody Preview (first 200 chars):")
    print(f"{email_msg.body[:200]}...")


def example_6_encoding_handling():
    """Example 6: Encoding detection and handling."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Encoding Detection")
    print("=" * 80)
    
    from main import EncodingManager
    
    # Test different encodings
    test_cases = [
        ('Hello World', 'utf-8'),
        ('Café français', 'utf-8'),
        ('Héllo Wörld', 'iso-8859-1'),
        ('日本語テキスト', 'utf-8'),
    ]
    
    for text, encoding in test_cases:
        # Encode and then detect
        encoded = text.encode(encoding)
        detected = EncodingManager.detect_and_decode(encoded)
        
        print(f"Original: {text}")
        print(f"Encoding: {encoding}")
        print(f"Detected: {detected}")
        print()


def example_7_pdf_generation():
    """Example 7: Direct PDF generation from EmailMessage."""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Direct PDF Generation")
    print("=" * 80)
    
    from main import EmailMessage, PDFGenerator
    from pathlib import Path
    
    # Create email message
    email = EmailMessage(
        subject='Test Email with HTML Content',
        sender='sender@example.com',
        recipients=['recipient@example.com'],
        cc=['cc@example.com'],
        bcc=[],
        date='2024-01-15 10:30:00',
        content_type='text/html',
        body='''<h2>Welcome to Mail2PDF NextGen</h2>
        <p>This email demonstrates HTML rendering capabilities.</p>
        <ul>
            <li>Feature 1: Multi-format support</li>
            <li>Feature 2: Robust encoding handling</li>
            <li>Feature 3: Professional PDF output</li>
        </ul>
        <p>Best regards,<br>The Mail2PDF Team</p>'''
    )
    
    # Generate PDF
    output_dir = Path('data/output/example7')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'generated_email.pdf'
    
    if PDFGenerator.generate(email, output_file):
        print(f"✓ PDF generated successfully: {output_file}")
    else:
        print("✗ PDF generation failed")


def example_8_utilities():
    """Example 8: Using utility functions."""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Utility Functions")
    print("=" * 80)
    
    from utils import (
        get_safe_filename,
        get_file_size_human,
        is_valid_email,
        extract_email_address,
        normalize_email_list,
        get_system_info
    )
    
    # Test safe filename
    unsafe_filename = "invalid<file>name|?.txt"
    safe = get_safe_filename(unsafe_filename)
    print(f"Original filename: {unsafe_filename}")
    print(f"Safe filename: {safe}")
    
    # Test file size formatting
    sizes = [1024, 1024 * 1024, 1024 * 1024 * 1024]
    print("\nFile sizes:")
    for size in sizes:
        print(f"  {size} bytes = {get_file_size_human(size)}")
    
    # Test email validation
    emails = [
        'valid@example.com',
        'invalid.email.com',
        'another@valid.co.uk'
    ]
    print("\nEmail validation:")
    for email in emails:
        print(f"  {email}: {is_valid_email(email)}")
    
    # Test email extraction
    text = "Contact us at support@example.com for help"
    extracted = extract_email_address(text)
    print(f"\nExtracted email from: '{text}'")
    print(f"Result: {extracted}")
    
    # Test email list normalization
    email_list = ['  USER@EXAMPLE.COM  ', 'John <john@example.com>', 'USER@EXAMPLE.COM']
    normalized = normalize_email_list(email_list)
    print(f"\nNormalized emails: {normalized}")
    
    # System info
    info = get_system_info()
    print(f"\nSystem Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")


def example_9_batch_conversion():
    """Example 9: Batch conversion with error handling."""
    print("\n" + "=" * 80)
    print("EXAMPLE 9: Batch Conversion with Error Handling")
    print("=" * 80)
    
    from pathlib import Path
    
    converter = EmailConverter()
    
    # Create output directory
    output_dir = Path('data/output/example9_batch')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert all EML files in input directory
    input_dir = Path('data/input')
    
    success_count = 0
    error_count = 0
    
    for eml_file in input_dir.glob('*.eml'):
        try:
            pdf_path = converter.convert_email(str(eml_file), str(output_dir))
            
            if pdf_path:
                print(f"✓ {eml_file.name} → {Path(pdf_path).name}")
                success_count += 1
            else:
                print(f"✗ {eml_file.name} - conversion failed")
                error_count += 1
        
        except Exception as e:
            print(f"✗ {eml_file.name} - error: {e}")
            error_count += 1
    
    print(f"\nResults: {success_count} succeeded, {error_count} failed")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("MAIL2PDF NEXTGEN - USAGE EXAMPLES")
    print("=" * 80)
    
    examples = [
        example_1_simple_conversion,
        example_2_directory_conversion,
        example_3_email_validation,
        example_4_custom_config,
        example_5_email_parsing,
        example_6_encoding_handling,
        example_7_pdf_generation,
        example_8_utilities,
        example_9_batch_conversion,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Example error: {e}")
            logger.error(f"Example {example_func.__name__} failed: {e}", exc_info=True)
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == '__main__':
    main()

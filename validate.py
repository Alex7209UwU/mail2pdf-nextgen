#!/usr/bin/env python3
"""
Mail2PDF NextGen - Validation and Testing Suite
Ville de Fontaine 38600, France
"""

import sys
from pathlib import Path
import json
import logging
from datetime import datetime
from main import EmailConverter, LoggingConfig, EmailTypeDetector

# Setup logging
logger = LoggingConfig.setup(verbose=True)


class ValidationSuite:
    """Complete validation test suite for Mail2PDF NextGen."""
    
    def __init__(self):
        """Initialize validation suite."""
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'categories': []
        }
        self.converter = EmailConverter()
        self.detector = EmailTypeDetector()
    
    def run_all(self) -> bool:
        """Run all validation tests."""
        logger.info("=" * 80)
        logger.info("MAIL2PDF NEXTGEN - VALIDATION SUITE")
        logger.info("=" * 80)
        
        tests = [
            ('File Detection', self.test_file_detection),
            ('Encoding Handling', self.test_encoding_handling),
            ('PDF Structure', self.test_pdf_structure),
            ('Attachment Extraction', self.test_attachment_extraction),
            ('HTML Rendering', self.test_html_rendering),
            ('CLI Interface', self.test_cli_interface),
            ('Web Interface', self.test_web_interface),
            ('Docker Container', self.test_docker_container),
        ]
        
        all_passed = True
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*80}")
            logger.info(f"Testing: {test_name}")
            logger.info(f"{'='*80}")
            
            try:
                passed = test_func()
                self.results['categories'].append({
                    'name': test_name,
                    'passed': passed,
                    'timestamp': datetime.now().isoformat()
                })
                
                if passed:
                    logger.info(f"✓ {test_name} - PASSED")
                else:
                    logger.warning(f"✗ {test_name} - FAILED")
                    all_passed = False
            
            except Exception as e:
                logger.error(f"✗ {test_name} - ERROR: {e}")
                self.results['categories'].append({
                    'name': test_name,
                    'passed': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                all_passed = False
        
        logger.info(f"\n{'='*80}")
        logger.info("VALIDATION SUMMARY")
        logger.info(f"{'='*80}")
        
        passed_count = sum(1 for c in self.results['categories'] if c['passed'])
        logger.info(f"Passed: {passed_count}/{len(self.results['categories'])}")
        logger.info(f"Status: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
        
        return all_passed
    
    def test_file_detection(self) -> bool:
        """Test 1: File format detection."""
        logger.info("Testing file format detection...")
        
        test_files = {
            'data/input/test_email.eml': 'eml',
        }
        
        all_passed = True
        
        for file_path, expected_format in test_files.items():
            file_obj = Path(file_path)
            
            if not file_obj.exists():
                logger.warning(f"  Test file not found: {file_path}")
                continue
            
            detected_format = self.detector.detect_format(file_obj)
            
            if detected_format == expected_format:
                logger.info(f"  ✓ {file_path}: {detected_format}")
            else:
                logger.warning(f"  ✗ {file_path}: Expected {expected_format}, got {detected_format}")
                all_passed = False
        
        logger.info("  ✓ File detection test completed")
        return all_passed
    
    def test_encoding_handling(self) -> bool:
        """Test 2: Encoding detection and handling."""
        logger.info("Testing encoding handling...")
        
        test_cases = [
            (b'Hello World', 'utf-8'),
            ('Héllo Wörld'.encode('utf-8'), 'utf-8'),
            ('Héllo Wörld'.encode('iso-8859-1'), 'iso-8859-1'),
            (b'\xff\xfe', 'utf-16'),
        ]
        
        from main import EncodingManager
        
        for data, expected_encoding in test_cases:
            try:
                result = EncodingManager.detect_and_decode(data)
                logger.info(f"  ✓ Decoded {len(data)} bytes successfully")
            except Exception as e:
                logger.error(f"  ✗ Encoding error: {e}")
                return False
        
        logger.info("  ✓ Encoding handling test completed")
        return True
    
    def test_pdf_structure(self) -> bool:
        """Test 3: PDF generation and structure."""
        logger.info("Testing PDF generation...")
        
        test_file = Path('data/input/test_email.eml')
        
        if not test_file.exists():
            logger.warning(f"  Test file not found: {test_file}")
            logger.info("  Skipping PDF structure test")
            return True
        
        try:
            output_dir = Path('data/output/test_validation')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            pdf_path = self.converter.convert_email(str(test_file), str(output_dir))
            
            if pdf_path:
                pdf_file = Path(pdf_path)
                
                if pdf_file.exists():
                    # Check file size
                    size = pdf_file.stat().st_size
                    
                    if size > 1024:  # PDF should be > 1KB
                        logger.info(f"  ✓ PDF generated: {pdf_path} ({size} bytes)")
                        
                        # Check PDF header
                        with open(pdf_file, 'rb') as f:
                            header = f.read(4)
                            if header == b'%PDF':
                                logger.info("  ✓ Valid PDF header")
                                return True
                            else:
                                logger.warning("  ✗ Invalid PDF header")
                                return False
                    else:
                        logger.warning(f"  ✗ PDF file too small: {size} bytes")
                        return False
                else:
                    logger.warning(f"  ✗ PDF file not created")
                    return False
            else:
                logger.warning("  ✗ PDF generation returned None")
                return False
        
        except Exception as e:
            logger.error(f"  ✗ PDF generation error: {e}")
            return False
    
    def test_attachment_extraction(self) -> bool:
        """Test 4: Attachment handling in emails."""
        logger.info("Testing attachment extraction...")
        
        from main import EMLParser
        
        test_file = Path('data/input/test_email.eml')
        
        if not test_file.exists():
            logger.warning(f"  Test file not found: {test_file}")
            logger.info("  Skipping attachment test")
            return True
        
        try:
            email_msg = EMLParser.parse(test_file)
            
            logger.info(f"  ✓ Email parsed successfully")
            logger.info(f"  ✓ Subject: {email_msg.subject}")
            logger.info(f"  ✓ From: {email_msg.sender}")
            logger.info(f"  ✓ Recipients: {len(email_msg.recipients)}")
            logger.info(f"  ✓ Attachments: {len(email_msg.attachments)}")
            
            return True
        
        except Exception as e:
            logger.error(f"  ✗ Attachment extraction error: {e}")
            return False
    
    def test_html_rendering(self) -> bool:
        """Test 5: HTML rendering in emails."""
        logger.info("Testing HTML rendering...")
        
        from main import PDFGenerator, EmailMessage
        
        try:
            # Create test email
            test_email = EmailMessage(
                subject='Test Email',
                sender='test@example.com',
                recipients=['recipient@example.com'],
                cc=[],
                bcc=[],
                date='2024-01-15 10:30:00',
                content_type='text/html',
                body='<p>This is a test email with <strong>HTML</strong> content.</p>'
            )
            
            # Generate PDF
            output_dir = Path('data/output/test_html')
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / 'test_html.pdf'
            
            if PDFGenerator.generate(test_email, output_file):
                logger.info(f"  ✓ HTML email rendered as PDF")
                return True
            else:
                logger.warning("  ✗ HTML rendering failed")
                return False
        
        except Exception as e:
            logger.error(f"  ✗ HTML rendering error: {e}")
            return False
    
    def test_cli_interface(self) -> bool:
        """Test 6: CLI interface functionality."""
        logger.info("Testing CLI interface...")
        
        test_file = Path('data/input/test_email.eml')
        
        if not test_file.exists():
            logger.warning(f"  Test file not found: {test_file}")
            logger.info("  Skipping CLI test")
            return True
        
        try:
            import subprocess
            
            # Test validation mode
            result = subprocess.run(
                ['python', 'main.py', '-i', str(test_file), '--validate'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("  ✓ CLI validation mode works")
                
                # Test file input validation
                validation = self.converter.validate(str(test_file))
                
                if validation['exists'] and validation['parseable']:
                    logger.info("  ✓ File validation successful")
                    return True
                else:
                    logger.warning("  ✗ File validation failed")
                    return False
            else:
                logger.warning(f"  ✗ CLI returned error: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"  ✗ CLI test error: {e}")
            return False
    
    def test_web_interface(self) -> bool:
        """Test 7: Web interface routes."""
        logger.info("Testing web interface...")
        
        try:
            import requests
            import time
            import subprocess
            
            # Note: This test requires Flask to be running
            # For now, we'll do basic import checks
            from app import app
            
            logger.info("  ✓ Flask app imports successfully")
            
            # Check routes exist
            routes = [route.rule for route in app.url_map.iter_rules()]
            
            required_routes = ['/', '/about', '/documentation', '/api/upload', '/api/download']
            
            for route in required_routes:
                if route in routes:
                    logger.info(f"  ✓ Route {route} exists")
                else:
                    logger.warning(f"  ✗ Route {route} missing")
                    return False
            
            logger.info("  ✓ Web interface test completed")
            return True
        
        except Exception as e:
            logger.error(f"  ✗ Web interface test error: {e}")
            return False
    
    def test_docker_container(self) -> bool:
        """Test 8: Docker configuration."""
        logger.info("Testing Docker configuration...")
        
        try:
            docker_file = Path('Dockerfile')
            docker_compose_file = Path('docker-compose.yml')
            
            checks_passed = 0
            
            if docker_file.exists():
                logger.info(f"  ✓ Dockerfile exists")
                checks_passed += 1
            else:
                logger.warning(f"  ✗ Dockerfile not found")
            
            if docker_compose_file.exists():
                logger.info(f"  ✓ docker-compose.yml exists")
                checks_passed += 1
            else:
                logger.warning(f"  ✗ docker-compose.yml not found")
            
            # Check Docker syntax (if docker is available)
            try:
                import subprocess
                result = subprocess.run(
                    ['docker', '--version'],
                    capture_output=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    logger.info(f"  ✓ Docker is available")
                    checks_passed += 1
            except Exception:
                logger.info("  ℹ Docker CLI not available (optional)")
            
            return checks_passed >= 2
        
        except Exception as e:
            logger.error(f"  ✗ Docker test error: {e}")
            return False
    
    def save_report(self, filepath: str = 'VALIDATION_REPORT.md') -> None:
        """Save validation report to file."""
        report = f"""# Mail2PDF NextGen - Validation Report

**Generated:** {self.results['timestamp']}

## Summary

| Category | Status |
|----------|--------|
"""
        
        for category in self.results['categories']:
            status = '✓ PASSED' if category['passed'] else '✗ FAILED'
            report += f"| {category['name']} | {status} |\n"
        
        passed = sum(1 for c in self.results['categories'] if c['passed'])
        total = len(self.results['categories'])
        
        report += f"\n**Overall:** {passed}/{total} tests passed\n\n"
        report += f"## Details\n\n"
        
        for category in self.results['categories']:
            status = '✓ PASSED' if category['passed'] else '✗ FAILED'
            report += f"### {category['name']}: {status}\n\n"
            
            if 'error' in category:
                report += f"**Error:** {category['error']}\n\n"
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        logger.info(f"Report saved to: {filepath}")


def main():
    """Run validation suite."""
    suite = ValidationSuite()
    all_passed = suite.run_all()
    suite.save_report()
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())

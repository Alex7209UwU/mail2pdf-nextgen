import unittest
import json
import os
import io
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app import app

class TestMail2PDF(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        
        # Setup specific test config
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = Path('./data/test_input')
        app.config['OUTPUT_FOLDER'] = Path('./data/test_output')
        app.config['SESSION_FOLDER'] = Path('./data/test_sessions')
        
        # Create directories
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], app.config['SESSION_FOLDER']]:
            folder.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.ctx.pop()
        # Clean up test directories (optional, maybe keep for inspection if failed)
        # shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)

    def create_dummy_eml(self):
        return (b'From: test@example.com\r\n'
                b'To: recipient@example.com\r\n'
                b'Subject: Test Email\r\n'
                b'\r\n'
                b'This is a test email body.')

    def test_home_page(self):
        """Test home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mail2PDF NextGen', response.data)

    def test_history_empty(self):
        """Test history endpoint returns empty list initially."""
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    @patch('main.EmailConverter.convert_email')
    def test_upload_flow(self, mock_convert):
        """Test file upload and conversion flow with options."""
        # Mock conversion to return a dummy PDF path
        mock_convert.return_value = 'dummy.pdf'

        data = {
            'files': (io.BytesIO(self.create_dummy_eml()), 'test.eml'),
            'extract_attachments': 'true',
            'page_size': 'Letter',
            'orientation': 'landscape'
        }
        
        response = self.client.post('/api/upload', data=data, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('session_id', result)
        self.assertEqual(result['files_processed'], 1)
        self.assertEqual(result['files_success'], 1)
        
        # Verify options were passed to converter
        # The first arg is file path, second is output dir, third is options
        args, kwargs = mock_convert.call_args
        self.assertEqual(args[2]['extract_attachments'], True)
        self.assertEqual(args[2]['page_size'], 'Letter')
        self.assertEqual(args[2]['orientation'], 'landscape')

    @patch('main.EmailConverter.get_preview_html')
    def test_preview_flow(self, mock_preview):
        """Test email preview endpoint."""
        mock_preview.return_value = "<html><body>Preview Content</body></html>"
        
        data = {
            'file': (io.BytesIO(self.create_dummy_eml()), 'preview.eml')
        }
        
        response = self.client.post('/api/preview', data=data, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['html'], "<html><body>Preview Content</body></html>")

    def test_configure_endpoint(self):
        """Test configuration endpoint loads."""
        response = self.client.get('/configure')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration', response.data)

if __name__ == '__main__':
    unittest.main()

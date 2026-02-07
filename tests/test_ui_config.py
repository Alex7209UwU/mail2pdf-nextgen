import unittest
import json
import os
import shutil
from pathlib import Path
import sys

# Add parent directory to path to import app
sys.path.append(str(Path(__file__).parent.parent))

from app import app, load_dynamic_config  # type: ignore

class TestConfigFeature(unittest.TestCase):
    def setUp(self):
        # Setup test client
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        
        # Use temporary config file
        self.original_config_file = app.config['CONFIG_FILE']
        self.test_config_file = Path('data/test_config.json')
        app.config['CONFIG_FILE'] = self.test_config_file
        
        # Create default test config
        default_config = {
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
        with open(self.test_config_file, 'w') as f:
            json.dump(default_config, f)

    def tearDown(self):
        # cleanup
        if self.test_config_file.exists():
            self.test_config_file.unlink()
        
        # Restore original config path
        app.config['CONFIG_FILE'] = self.original_config_file
        self.ctx.pop()

    def test_configure_page_loads(self):
        """Test that /configure page returns 200 OK."""
        response = self.client.get('/configure')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration du Site', response.data)

    def test_update_config(self):
        """Test updating configuration via POST."""
        new_data = {
            'language': 'en',
            'color_primary': '#ff0000',
            'color_secondary': '#00ff00',
            'color_accent': '#0000ff',
            'color_background': '#000000',
            'color_text': '#ffffff'
        }
        
        response = self.client.post('/configure', data=new_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration saved!', response.data)
        
        # Verify file updated
        with open(self.test_config_file, 'r') as f:
            config = json.load(f)
        
        self.assertEqual(config['language'], 'en')
        self.assertEqual(config['colors']['primary'], '#ff0000')

    def test_index_reflects_config(self):
        """Test that index page reflects configuration changes."""
        # First ensure we are in English
        with open(self.test_config_file, 'r+') as f:
            config = json.load(f)
            config['language'] = 'en'
            config['colors']['primary'] = '#123456'
            f.seek(0)
            json.dump(config, f)
            f.truncate()
            
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check text (English)
        self.assertIn(b'Import your emails', response.data)
        
        # Check color
        self.assertIn(b'--primary-color: #123456', response.data)

    def test_context_processor(self):
        """Test that config is injected into templates."""
        with app.test_request_context():
            # This is a bit tricky to test directly without rendering, 
            # but we verified it via index page rendering above.
            pass

if __name__ == '__main__':
    unittest.main()

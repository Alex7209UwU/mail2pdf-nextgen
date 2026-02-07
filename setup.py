#!/usr/bin/env python3
"""
Mail2PDF NextGen - Setup.py for Package Installation
Ville de Fontaine 38600, France
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme = Path('README.md').read_text(encoding='utf-8') if Path('README.md').exists() else ''

setup(
    name='mail2pdf-nextgen',
    version='1.0.0',
    description='Advanced Email to PDF Converter with multi-format support',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ville de Fontaine 38600',
    author_email='dev@example.com',
    url='https://github.com/yourusername/mail2pdf-nextgen',
    license='MIT',
    python_requires='>=3.8',
    py_modules=['main', 'app', 'config', 'utils'],
    entry_points={
        'console_scripts': [
            'mail2pdf=main:main',
        ],
    },
    install_requires=[
        'extract-msg>=0.41.1',
        'weasyprint>=60.0',
        'tinycss2>=1.2.1',
        'cffi>=1.15.0',
        'Pillow>=9.0.0',
        'chardet>=5.0.0',
        'Flask>=2.0.0',
        'Werkzeug>=2.0.0',
    ],
    extras_require={
        'dev': ['pytest>=7.0.0', 'black>=22.0.0', 'flake8>=4.0.0'],
        'docker': [],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
        'Topic :: Communications :: Email',
    ],
    keywords='email pdf converter eml msg mbox thunderbird',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/mail2pdf-nextgen/issues',
        'Source': 'https://github.com/yourusername/mail2pdf-nextgen',
        'Documentation': 'https://github.com/yourusername/mail2pdf-nextgen/blob/main/README.md',
    },
)

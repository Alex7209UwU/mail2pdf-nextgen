import os
from pathlib import Path
import tempfile
import pytest

from main import EmailTypeDetector, EncodingManager, EMLParser, EmailConverter


def test_detect_format_eml(tmp_path):
    f = tmp_path / "test.eml"
    f.write_bytes(b"From: a@b.com\nTo: c@d.com\nSubject: Hi\n\nBody")
    assert EmailTypeDetector.detect_format(f) == 'eml'


def test_encoding_detect_and_decode():
    b = 'Caf\xe9'.encode('latin-1')
    s = EncodingManager.detect_and_decode(b)
    assert 'Caf' in s


def test_eml_parse_minimal(tmp_path):
    f = tmp_path / "test.eml"
    f.write_bytes(b"From: a@b.com\nTo: c@d.com\nSubject: Test\n\nHello world")
    msg = EMLParser.parse(f)
    assert msg.subject == 'Test' or 'Test' in msg.subject
    assert 'Hello world' in msg.body


def test_convert_email_no_input(tmp_path):
    conv = EmailConverter()
    result = conv.convert_email(str(tmp_path / "nope.eml"), str(tmp_path))
    assert result is None

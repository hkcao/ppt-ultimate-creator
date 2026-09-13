"""Run with Python, PyMuPDF and unittest; all outputs stay in a temporary directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import pymupdf as fitz

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/ppt-ultimate-creator/scripts'


class Helpers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pdf = self.root / 'source.pdf'
        with fitz.open() as doc:
            page = doc.new_page(width=400, height=300)
            page.insert_text((30, 50), 'Baseline 120 ms; new 84 ms')
            page.insert_text((30, 250), 'Outside crop')
            doc.new_page(width=400, height=300)
            doc.save(self.pdf)

    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True)

    def test_pdf_crop_and_provenance(self):
        out = self.root / 'extract'
        result = self.run_script('extract_pdf.py', self.pdf, out, '--pages', '1', '--clip', 0, 0, 400, 100)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (out / 'page-001.txt').read_text()
        self.assertIn('120 ms', text)
        self.assertNotIn('Outside crop', text)
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['source_sha256'], hashlib.sha256(self.pdf.read_bytes()).hexdigest())
        self.assertEqual(manifest['pages'][0]['clip'], [0, 0, 400, 100])
        self.assertGreater((out / 'page-001.png').stat().st_size, 100)
        self.assertNotEqual(self.run_script('extract_pdf.py', self.pdf, out, '--pages', '1').returncode, 0)

    def test_invalid_page_does_not_write(self):
        out = self.root / 'bad'
        self.assertNotEqual(self.run_script('extract_pdf.py', self.pdf, out, '--pages', '3').returncode, 0)
        self.assertFalse(out.exists())

    def test_html_preserves_and_escapes_content(self):
        spec = self.root / 'slides.json'
        spec.write_text(json.dumps({'slides': [{'id': 's01', 'title': '<script>alert(1)</script>',
            'content': [{'text': '120 ms → 84 ms'}], 'layout': 'two columns'}]}))
        out = self.root / 'html'
        result = self.run_script('storyboard.py', spec, out)
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (out / 'deck.html').read_text()
        self.assertIn('120 ms → 84 ms', html)
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        before = (out / 'deck.html').read_bytes()
        self.assertNotEqual(self.run_script('storyboard.py', spec, out).returncode, 0)
        self.assertEqual(before, (out / 'deck.html').read_bytes())


if __name__ == '__main__':
    unittest.main()

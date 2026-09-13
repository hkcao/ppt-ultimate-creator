import base64
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

path = Path(__file__).resolve().parents[1] / 'skills/ppt-ultimate-creator/scripts/generate_image.py'
spec = importlib.util.spec_from_file_location('generate_image', path)
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)


class ImageBackend(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / 'v1'
        buffer = io.BytesIO()
        Image.new('RGB', (8, 6), 'blue').save(buffer, format='PNG')
        self.png = buffer.getvalue()
        self.config = dict(endpoint='https://provider.example/v1/images/generations', model='external-model',
                           api_key_env='TEST_PPT_KEY')
        env = patch.dict(os.environ, {'TEST_PPT_KEY': 'fake-test-secret'})
        env.start()
        self.addCleanup(env.stop)

    def test_base64_request_and_safe_record(self):
        response = json.dumps({'data': [{'b64_json': base64.b64encode(self.png).decode()}]}).encode()
        with patch.object(backend, 'fetch', return_value=response) as fetch:
            result = backend.generate(self.config, 'A slide', self.output)
        payload = json.loads(fetch.call_args.args[1])
        self.assertEqual(payload, {'model': 'external-model', 'prompt': 'A slide', 'n': 1})
        self.assertTrue(result.exists())
        record = (self.output / 'record.json').read_text()
        self.assertNotIn('fake-test-secret', record)
        self.assertNotIn('A slide', record)
        with patch.object(backend, 'fetch') as fetch:
            with self.assertRaises(ValueError):
                backend.generate(self.config, 'Again', self.output)
            fetch.assert_not_called()

    def test_url_download_does_not_forward_key(self):
        response = json.dumps({'data': [{'url': 'https://cdn.example/image.png?signature=secret'}]}).encode()
        with patch.object(backend, 'fetch', side_effect=[response, self.png]) as fetch:
            backend.generate(self.config, 'A slide', self.output)
        self.assertNotIn('key', fetch.call_args.kwargs)
        self.assertEqual(len(fetch.call_args.args), 1)
        self.assertNotIn('signature', (self.output / 'record.json').read_text())

    def test_bad_image_is_not_saved(self):
        response = json.dumps({'data': [{'b64_json': base64.b64encode(b'not an image').decode()}]}).encode()
        with patch.object(backend, 'fetch', return_value=response):
            with self.assertRaises(Exception):
                backend.generate(self.config, 'A slide', self.output)
        self.assertFalse(self.output.exists())

    def test_missing_key_and_unsafe_url_do_not_request(self):
        for cfg in [dict(self.config, api_key_env='UNSET_TEST_PPT_KEY'),
                    dict(self.config, endpoint='http://provider.example/generate')]:
            with patch.object(backend, 'fetch') as fetch:
                with self.assertRaises(ValueError):
                    backend.generate(cfg, 'A slide', self.output)
                fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()

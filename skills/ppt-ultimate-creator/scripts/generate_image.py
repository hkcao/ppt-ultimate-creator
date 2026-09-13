"""Generate one image via a user-configured compatible Images API. Requires Pillow."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from PIL import Image


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect refused; configure the final HTTPS endpoint')


def check_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password or parts.fragment:
        raise ValueError('Expected HTTPS URL without embedded credentials or fragment')


def fetch(url, body=None, key=None, timeout=180):
    check_url(url)
    headers = {'Content-Type': 'application/json'} if body is not None else {}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    request = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        data = response.read(64 * 1024 * 1024 + 1)
    if len(data) > 64 * 1024 * 1024:
        raise ValueError('Response exceeds 64 MiB')
    return data


def generate(config, prompt, output):
    if output.exists():
        raise ValueError('Output already exists; choose a new version directory')
    endpoint = config['endpoint']
    check_url(endpoint)
    if urllib.parse.urlsplit(endpoint).query:
        raise ValueError('Endpoint must not contain query credentials')
    key = os.environ.get(config['api_key_env'])
    if not key:
        raise ValueError('Configured API key environment variable is unset')
    params = config.get('parameters', {})
    if {'model', 'prompt', 'n'} & params.keys():
        raise ValueError('parameters must not override model, prompt or n')
    payload = dict(params, model=config['model'], prompt=prompt, n=1)
    raw = fetch(endpoint, json.dumps(payload).encode(), key, config.get('timeout', 180))
    item = json.loads(raw)['data'][0]
    if item.get('b64_json'):
        image = base64.b64decode(item['b64_json'], validate=True)
    elif item.get('url'):
        # Download generated output without forwarding API credentials.
        image = fetch(item['url'], timeout=config.get('timeout', 180))
    else:
        raise ValueError('Expected data[0].b64_json or data[0].url')
    with Image.open(io.BytesIO(image)) as picture:
        picture.verify()
    with Image.open(io.BytesIO(image)) as picture:
        size = picture.size
        output.mkdir(parents=True)
        picture.save(output / 'image.png')
    record = dict(model=config['model'], endpoint_host=urllib.parse.urlsplit(endpoint).hostname,
                  prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                  config_sha256=hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
                  image_sha256=hashlib.sha256((output / 'image.png').read_bytes()).hexdigest(), size=size)
    (output / 'record.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    return output / 'image.png'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path.home() / '.ppt-ultimate-creator/image-api.json')
    parser.add_argument('--prompt', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = generate(json.loads(args.config.read_text()), args.prompt.read_text(), args.output)
    except urllib.error.HTTPError as error:
        parser.exit(1, f'Image API HTTP {error.code}; no automatic retry.\n')
    except Exception as error:
        # Provider bodies/URLs can contain prompt text or signed credentials.
        parser.exit(1, f'Image generation failed ({type(error).__name__}); check config, key environment and provider status. No automatic retry.\n')
    print(result)


if __name__ == '__main__':
    main()

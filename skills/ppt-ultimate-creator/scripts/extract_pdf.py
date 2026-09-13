"""Batch render evidence. Coordinates are PDF points, origin at top-left."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--pages', required=True, help='1-based comma-separated pages, e.g. 2,4,5')
    parser.add_argument('--clip', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'))
    parser.add_argument('--dpi', type=int, default=160)
    args = parser.parse_args()
    import pymupdf as fitz
    pages = list(dict.fromkeys(int(x) for x in args.pages.split(',')))
    if args.dpi <= 0:
        parser.error('dpi must be positive')
    with fitz.open(args.pdf) as doc:
        if not pages or any(n < 1 or n > len(doc) for n in pages):
            parser.error('page outside document')
        clips = []
        for n in pages:
            rect = fitz.Rect(args.clip) if args.clip else doc[n - 1].rect
            if rect.is_empty or rect.is_infinite or not doc[n - 1].rect.contains(rect):
                parser.error('clip must be a nonempty rectangle inside every selected page')
            clips.append(rect)
        if args.output.exists() and any(args.output.iterdir()):
            parser.error('output must be empty; choose a new version directory')
        args.output.mkdir(parents=True, exist_ok=True)
        records = []
        for n, rect in zip(pages, clips):
            page = doc[n - 1]
            name = f'page-{n:03}.png'
            page.get_pixmap(dpi=args.dpi, clip=rect).save(args.output / name)
            (args.output / f'page-{n:03}.txt').write_text(page.get_text(clip=rect), encoding='utf-8')
            records.append(dict(page=n, clip=list(rect), image=name,
                                image_sha256=hashlib.sha256((args.output / name).read_bytes()).hexdigest()))
        manifest = dict(source=str(args.pdf.resolve()), source_sha256=hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
                        dpi=args.dpi, pages=records)
        (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Extracted {len(records)} pages; verify crops against the source.')


if __name__ == '__main__':
    main()

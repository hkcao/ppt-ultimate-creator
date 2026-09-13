"""Render low-fidelity draft content: {slides:[{id,title,content:[{text}],layout}]}.

Use the current slides.yaml draft converted to JSON; review outline and HTML together.
"""
import argparse
import html
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    slides = json.loads(args.spec.read_text(encoding='utf-8'))['slides']
    if not slides:
        parser.error('slides must not be empty')
    if args.output.exists() and any(args.output.iterdir()):
        parser.error('output must be empty; choose a new version directory')
    escape = lambda value: html.escape(str(value))
    sections = []
    for i, slide in enumerate(slides, 1):
        items = ''.join(f'<li>{escape(item["text"])}</li>' for item in slide.get('content', []))
        sections.append(f'<section><small>{i} · {escape(slide["id"])}</small><h1>{escape(slide["title"])}</h1>'
                        f'<ul>{items}</ul><aside>布局意图（待实现）：{escape(slide.get("layout", ""))}</aside></section>')
    style = '''body{margin:24px;background:#eee;font-family:"Times New Roman","Microsoft YaHei",serif}
section{box-sizing:border-box;aspect-ratio:16/9;width:min(100%,1100px);margin:24px auto;padding:4%;background:white;overflow:auto}
h1{font-size:clamp(22px,3vw,40px)}li{font-size:clamp(16px,2vw,28px);margin:1em 0}aside,small{color:#555}
@media print{section{break-after:page;margin:0;width:100%}}'''
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'deck.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>内容草稿</title><style>'
        + style + '</style><body><p>内容检查草稿；布局意图尚未实现，不能作为布局确认稿或 AI 视觉稿。</p>'
        + ''.join(sections) + '</body></html>', encoding='utf-8')
    print(f'Rendered {len(slides)} slides. Implement and review intended layouts before layout approval.')


if __name__ == '__main__':
    main()

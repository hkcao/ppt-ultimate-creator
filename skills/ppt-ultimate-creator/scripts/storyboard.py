"""Write lofi.md from current slide-spec JSON; review outline and blueprint together.

Each slide needs id, title, blueprint (ASCII text), and visual_guidance (text list).
Optional fields mirror slides.yaml; this script does not invent layouts or render HTML.
"""
import argparse
import json
from pathlib import Path


def block(value, language='text'):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    fence = '```'
    while fence in text:
        fence += '`'
    return f'{fence}{language}\n{text}\n{fence}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding='utf-8'))
    slides = spec['slides']
    if not slides:
        parser.error('slides must not be empty')
    for slide in slides:
        blueprint = slide.get('blueprint')
        guidance = slide.get('visual_guidance')
        if not isinstance(blueprint, str) or not blueprint.strip():
            parser.error(f'{slide["id"]}: blueprint must contain the authored ASCII layout')
        if not isinstance(guidance, list) or not guidance or any(
                not isinstance(item, str) or not item.strip() for item in guidance):
            parser.error(f'{slide["id"]}: visual_guidance must be a non-empty list of text')
    if args.output.exists() and any(args.output.iterdir()):
        parser.error('output must be empty; choose a new version directory')
    sections = ['# 低保真蓝图', '内容与区域布局确认稿；精细视觉在 AI 样张阶段确认。']
    # Preserve all global requirements without manufacturing defaults or approvals.
    sections.extend(['## 全局要求', block({k: v for k, v in spec.items() if k != 'slides'}, 'json')])
    for i, slide in enumerate(slides, 1):
        sections.extend([f'## P{i}',
                         '### 逐页内容与依据',
                         block({k: v for k, v in slide.items()
                                if k not in ('blueprint', 'visual_guidance')}, 'json'),
                         '### 区域蓝图', block(slide['blueprint']),
                         '### 视觉指引', block('\n'.join('- ' + item for item in slide['visual_guidance']))])
    sections.extend(['## 生图总指引',
                     '沿用 brief 的共享风格、模板固定项、画幅和密度；逐页一张独立图，'
                     '输出到 visuals/。内容以当前规格为准，不改写数字、公式和引用。'
                     '先按技能流程确认蓝图，再生成代表性样张；此文件生成不代表用户已确认。',
                     '### 逐页生成清单',
                     block([{'page': i, 'id': slide['id'], 'title': slide['title'],
                             'presentation': slide.get('presentation'),
                             'assets': slide.get('assets', [])}
                            for i, slide in enumerate(slides, 1)], 'json')])
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'lofi.md').write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
    print(f'Wrote {len(slides)} page blueprints to {args.output / "lofi.md"}; awaiting review.')


if __name__ == '__main__':
    main()

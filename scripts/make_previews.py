#!/usr/bin/env python3
"""Present existing logo exports on matching boards; never modify logo assets."""
from pathlib import Path
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SIZE = (2200, 1430)
PAPER = '#fbf7ef'
INK = '#3e292a'
MUTED = '#8a7772'
RULE = '#d9cfc4'
SANS = Path(os.environ.get(
    'PREVIEW_SANS_FONT', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'))
SERIF = Path(os.environ.get(
    'PREVIEW_SERIF_FONT', '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'))

PROJECTS = {
    'collegium-magicarum-scientiarum-logo': {
        'name': 'COLLEGIUM MAGICARUM SCIENTIARUM',
        'title': '猫头鹰与羽毛笔',
        'subtitle': '古典书票纹样  ·  酒红火漆',
        'accent': '#932e3b',
        'panels': (
            ('owl-quill-wax-seal-transparent.png', '01   标准图形',
             '交织卷枝 × 叶饰花结  ·  Litt. / Phil.'),
            ('owl-quill-wax-seal-embossed.png', '02   火漆浮雕',
             '同色压印  ·  不规则蜡唇  ·  柔和侧光'),
        ),
    },
    'institutum-scientiae-magicae-logo': {
        'name': 'INSTITUTUM SCIENTIAE MAGICAE',
        'title': '猫头鹰与圆规',
        'subtitle': '博物学版画  ·  墨绿与黄铜金',
        'accent': '#183c34',
        'panels': (
            ('logo-preview.png', '01   主徽章',
             '完整拉丁环文  ·  猫头鹰与圆规  ·  新艺术植物饰边'),
            ('logo-icon-1600.png', '02   无文字副章',
             '保留版画主体与仪器  ·  适用于较小尺寸'),
        ),
    },
}


def font(size, serif=False):
    file = SERIF if serif else SANS
    if not file.is_file():
        variable = 'PREVIEW_SERIF_FONT' if serif else 'PREVIEW_SANS_FONT'
        raise FileNotFoundError(f'Set {variable} to an installed Noto CJK font: {file}')
    return ImageFont.truetype(str(file), size)


def make_preview(project):
    spec = PROJECTS[project]
    folder = ROOT / project
    board = Image.new('RGBA', SIZE, PAPER)
    draw = ImageDraw.Draw(board)
    draw.text((112, 62), spec['name'], fill=spec['accent'], font=font(22))
    draw.text((108, 106), spec['title'], fill=INK, font=font(60, True))
    draw.text((1260, 128), spec['subtitle'], fill=MUTED, font=font(26))
    draw.line((112, 222, 2088, 222), fill=RULE, width=2)

    for x, (filename, title, caption) in zip((100, 1140), spec['panels']):
        # Fit the complete original square canvas. Never crop, recolour,
        # adjust opacity, change composition or scale nonuniformly.
        with Image.open(folder / 'png' / filename) as original:
            image = original.convert('RGBA')
            if image.width != image.height:
                raise ValueError(f'Expected square logo canvas: {filename}')
            image = image.resize((960, 960), Image.Resampling.LANCZOS)
            board.alpha_composite(image, (x, 266))
        draw.text((x + 18, 1250), title, fill=INK, font=font(29, True))
        draw.text((x + 18, 1302), caption, fill=MUTED, font=font(22))

    output = folder / 'design-preview.png'
    temporary = output.with_suffix('.png.tmp')
    board.convert('RGB').save(temporary, format='PNG')
    temporary.replace(output)
    print(output.relative_to(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', choices=PROJECTS, help='Only regenerate one board')
    args = parser.parse_args()
    for project in (args.project,) if args.project else PROJECTS:
        make_preview(project)


if __name__ == '__main__':
    main()

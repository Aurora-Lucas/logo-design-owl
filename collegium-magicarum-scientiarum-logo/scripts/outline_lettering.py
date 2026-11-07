#!/usr/bin/env python3
"""Outline California sun lettering from the supplied font; Cairo/Pango required.
The generated lettering.svg is self-contained, and build_seal.py only needs stdlib.
"""
from pathlib import Path
import os
import ctypes
import ctypes.util
import xml.etree.ElementTree as ET
import cairo
import gi

gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
def tag(name): return '{' + NS + '}' + name

font_path = os.environ.get('CALIFORNIA_SUN_FONT')
if not font_path:
    raise RuntimeError('Set CALIFORNIA_SUN_FONT to your independently licensed California sun font file')
fontfile = Path(font_path).expanduser()
fontconfig = ctypes.CDLL(ctypes.util.find_library('fontconfig'))
fontconfig.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
fontconfig.FcConfigAppFontAddFile.restype = ctypes.c_int
if not fontconfig.FcConfigAppFontAddFile(None, str(fontfile).encode()):
    raise RuntimeError('Cannot register the supplied California sun font')

svg = ET.Element(tag('svg'), {'viewBox': '0 0 1024 1024', 'width': '1024', 'height': '1024'})
ET.SubElement(svg, tag('title')).text = 'Litt. and Phil. — California sun outlined lettering'
ET.SubElement(svg, tag('desc')).text = (
    'Litt. stands for litteratura; Phil. stands for philosophia. '
    'Outlined from the user-supplied California-sun-2.otf, matching the staggered reference placement.'
)
group = ET.SubElement(svg, tag('g'), {'id': 'side-lettering', 'fill': 'white'})
context = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
# Disable hinting so the vector curves preserve the font's actual proportions.
options = cairo.FontOptions()
options.set_hint_style(cairo.HINT_STYLE_NONE)
options.set_hint_metrics(cairo.HINT_METRICS_OFF)
context.set_font_options(options)
font = Pango.FontDescription()
font.set_family('California sun')
font.set_absolute_size(84 * Pango.SCALE)

def number(n):
    return f'{n:.6f}'.rstrip('0').rstrip('.') or '0'

for text, ident, center, meaning in [
    ('Litt.', 'lettering-litt', (317, 458), 'litteratura'),
    ('Phil.', 'lettering-phil', (708, 624), 'philosophia'),
]:
    layout = PangoCairo.create_layout(context)
    layout.set_font_description(font)
    layout.set_text(text, -1)
    resolved = layout.get_context().load_font(font).describe().get_family()
    if resolved != 'California sun':
        raise RuntimeError(f'Unexpected fallback font: {resolved}')
    context.new_path()
    context.move_to(0, 0)
    PangoCairo.layout_path(context, layout)
    x0, y0, x1, y1 = context.path_extents()
    offset_x = center[0] - (x0+x1)/2
    offset_y = center[1] - (y0+y1)/2
    parts = []
    for kind, values in context.copy_path():
        if kind == cairo.PATH_CLOSE_PATH:
            parts.append('Z')
        else:
            command = {cairo.PATH_MOVE_TO: 'M', cairo.PATH_LINE_TO: 'L', cairo.PATH_CURVE_TO: 'C'}[kind]
            points = []
            for i in range(0, len(values), 2):
                points.append(number(values[i]+offset_x) + ',' + number(values[i+1]+offset_y))
            parts.append(command + ' '.join(points))
    label = ET.SubElement(group, tag('g'), {'id': ident, 'aria-label': text})
    ET.SubElement(label, tag('title')).text = f'{text} — {meaning}'
    ET.SubElement(label, tag('path'), {'d': ' '.join(parts), 'fill-rule': 'nonzero'})
    print(text, 'visible bounds:', tuple(round(v, 3) for v in (x0+offset_x, y0+offset_y, x1+offset_x, y1+offset_y)))

ET.indent(svg, space='  ')
ET.ElementTree(svg).write(ROOT / 'assets/lettering.svg', encoding='utf-8', xml_declaration=True)

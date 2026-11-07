"""Extract the public-domain owl engraving as single-colour SVG geometry.

Source: The Metropolitan Museum of Art, The Great White Owl, 1771,
Anonymous British, 1999.291.3, public domain.
https://www.metmuseum.org/art/collection/search/750817
Image: https://images.metmuseum.org/CRDImages/dp/original/DP879141.jpg

Input is assets/owl-source-public-domain.jpg. Python runtime requires Pillow,
NumPy, and vtracer installed in the active Python environment.
The hand-drawn contour is recorded in coordinates of the 740px reference.
Threshold is a local paper-luminance difference, preserving fine engraving.
"""
from pathlib import Path
import sys
import re
import xml.etree.ElementTree as ET
import vtracer
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
GREEN = '#183C34'
im = Image.open(OUT / 'owl-source-public-domain.jpg').convert('RGB')
scale = im.width / 740

# Clockwise: crown, back, folded flight feathers, tail, short perch, breast.
# The original trunk, scenery, plate title, and paper margins are excluded.
contour = [
    (175,392),(176,377),(176,362),(181,347),(176,332),(184,317),
    (198,305),(218,294),(237,287),(257,288),(274,294),(289,304),
    (303,319),(315,339),(323,360),(327,385),(332,402),(337,418),
    (353,420),(373,427),(397,441),(420,453),(443,470),(467,489),
    (490,511),(513,537),(535,567),(554,599),(574,633),(592,668),
    (609,706),(625,745),(638,785),(646,817),(652,845),(657,864),
    (648,854),(635,840),(618,819),(601,796),(585,772),(571,750),
    (563,772),(549,791),(533,801),(516,804),(497,799),(480,790),
    (461,777),(451,768),(443,754),(426,754),(406,751),(389,747),
    (370,746),(351,743),(334,742),(319,742),(335,759),(357,778),
    (381,799),(400,817),(402,823),(393,819),(371,803),(348,784),
    (326,764),(309,746),(294,737),(280,734),(263,735),(245,734),
    (231,731),(221,725),(218,716),(222,707),(234,702),(248,700),
    (266,696),(279,690),(262,681),(245,669),(225,653),(206,640),
    (184,625),(167,611),(150,592),(137,572),(130,550),(127,527),
    (128,504),(131,481),(137,464),(146,452),(158,448),(171,450),
    (178,442),(179,429),(178,417),(173,405),
]
mask = Image.new('L', im.size, 0)
draw = ImageDraw.Draw(mask)
poly = [(round(x*scale), round(y*scale)) for x,y in contour]
draw.polygon(poly, fill=255)

gray = im.convert('L')
# Radius 18 px is about 8.6 px at the 740px reference size: larger than the
# engraved lines but smaller than paper illumination gradients.
paper = gray.filter(ImageFilter.GaussianBlur(18))
g = np.asarray(gray).astype(np.float32)
b = np.asarray(paper).astype(np.float32)
inside = np.asarray(mask) > 0
# Fine light feather strokes are locally dark even when brighter than old ink.
ink = ((b-g > 8.5) | (g < 122)) & inside
box = mask.getbbox()
# Slight external padding, shared by detail and silhouette SVGs.
box = (box[0]-5, box[1]-5, box[2]+5, box[3]+5)
ink = ink[box[1]:box[3], box[0]:box[2]]
cropped_mask = mask.crop(box)
binary = Image.fromarray(np.where(ink, 0, 255).astype('uint8'), 'L')
binary.save(OUT / 'owl-engraving-bw.png')
cropped_mask.save(OUT / 'owl-silhouette-mask.png')

# vtracer's binary mode traces only the ink, giving scalable filled contours.
vtracer.convert_image_to_svg_py(
    str(OUT / 'owl-engraving-bw.png'), str(OUT / 'owl-engraving.svg'),
    colormode='binary', mode='spline', filter_speckle=2,
    corner_threshold=70, length_threshold=3.5, max_iterations=10,
    splice_threshold=45, path_precision=2,
)
svg = (OUT / 'owl-engraving.svg').read_text()
svg = svg.replace('fill="#000000"', f'fill="{GREEN}"')
width,height = binary.size
svg = svg.replace(f'width="{width}" height="{height}"', f'width="{width}" height="{height}" viewBox="0 0 {width} {height}"')
svg = svg.replace('<svg ', '<svg role="img" aria-label="Owl engraving after The Great White Owl, 1771" ',1)
(OUT / 'owl-engraving.svg').write_text(svg)

# The silhouette uses the same hand-drawn perimeter and exact viewBox.
points = ' '.join(f'{x-box[0]:.1f},{y-box[1]:.1f}' for x,y in poly)
(OUT / 'owl-silhouette.svg').write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    f'<polygon fill="{GREEN}" points="{points}"/></svg>\n'
)
print(f'Wrote owl vector and silhouette, viewBox="0 0 {width} {height}"; crop={box}; ink={ink.sum()} pixels')

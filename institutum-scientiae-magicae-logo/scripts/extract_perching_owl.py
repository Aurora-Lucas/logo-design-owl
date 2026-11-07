"""Remove the original wooden perch while retaining toes and tail feathers.

The input engraving is the public-domain Met image processed by extract_owl.py.
This script keeps its exact 1122 x 1220 canvas so the replacement instrument
can be aligned consistently. Cut polygons are in that cropped canvas space.

The narrow diagonal below the left foot is a tail feather, not a branch, and
is deliberately retained. The cuts remove the bare rail between the feet
and the downward-curving wood outside the right toes. Small contact strokes
immediately under the talons remain so a metal rail can cover them naturally.
"""
from pathlib import Path
import sys
import vtracer
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
INK = '#183C34'

CUTS = [
    # The exposed section between the two feet, preserving the left hook.
    [(390,887),(411,889),(439,893),(463,898),(456,914),
     (449,930),(456,943),(473,958),(448,961),(423,955),
     (399,954),(390,944)],
    # Clear wood inside the left talon's hook without removing its outer arc.
    [(362,905),(383,906),(397,916),(395,934),(381,935),
     (369,931),(363,923)],
    # Isolated upper and lower contours of the former bare branch.
    [(418,885),(451,887),(471,897),(464,904),(444,898),(425,895)],
    [(410,952),(435,952),(440,961),(412,961)],
    # The bent tree trunk beyond the rightmost toes.
    [(682,959),(704,951),(726,956),(749,968),(776,1000),
     (799,1041),(823,1086),(805,1103),(775,1103),
     (745,1082),(712,1054),(695,1032),(679,1015),
     (674,980)],
]

binary = Image.open(ASSETS / 'owl-engraving-bw.png').convert('L')
silhouette = Image.open(ASSETS / 'owl-silhouette-mask.png').convert('L')
assert binary.size == silhouette.size == (1122,1220)
draw = ImageDraw.Draw(binary)
sd = ImageDraw.Draw(silhouette)
for polygon in CUTS:
    draw.polygon(polygon, fill=255)
    sd.polygon(polygon, fill=0)
binary.save(ASSETS / 'owl-perching-bw.png')
silhouette.save(ASSETS / 'owl-perching-silhouette-mask.png')

def trace(png, svg, is_silhouette=False):
    vtracer.convert_image_to_svg_py(
        str(png), str(svg), colormode='binary', mode='spline',
        filter_speckle=2, corner_threshold=70, length_threshold=3.5,
        max_iterations=10, splice_threshold=45, path_precision=2,
    )
    s=svg.read_text().replace('fill="#000000"',f'fill="{INK}"')
    s=s.replace('width="1122" height="1220"','width="1122" height="1220" viewBox="0 0 1122 1220"')
    svg.write_text(s)

trace(ASSETS / 'owl-perching-bw.png', ASSETS / 'owl-perching.svg')
# vtracer traces black ink; invert the white silhouette mask for this pass.
inv = Image.eval(silhouette, lambda x: 255-x)
inv.save(ASSETS / 'owl-perching-silhouette-trace.png')
trace(ASSETS / 'owl-perching-silhouette-trace.png', ASSETS / 'owl-perching-silhouette.svg', True)

# Enlarged comparison, for checking toes against the replacement rail.
before=Image.open(ASSETS/'owl-engraving-bw.png').convert('RGB').crop((150,840,850,1100))
after=binary.convert('RGB').crop((150,840,850,1100))
comparison=Image.new('RGB',(1400,520),'white')
comparison.paste(before.resize((1400,520)),(0,0))
after.resize((1400,520)).save(ASSETS/'owl-perching-feet-detail.png')
print('Wrote owl-perching.svg and matching silhouette with unchanged canvas.')

#!/usr/bin/env python3
"""Build the editable seal family from SVG geometry, using the preserved owl source component.
Run: python3 scripts/build_seal.py
No third party packages are required. PNG export is separate (scripts/export.mjs).
"""
from pathlib import Path
from copy import deepcopy
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
def tag(n): return '{'+NS+'}'+n

def smooth_edge():
    points=[]
    for i in range(96):
        t=2*math.pi*i/96
        r=477+5*math.sin(5*t+.6)+3.8*math.sin(9*t+1.1)+2.6*math.sin(13*t-.5)
        points.append((512+r*math.cos(t),512+r*math.sin(t)))
    def xy(p): return f'{p[0]:.2f},{p[1]:.2f}'
    d='M'+xy(points[0])
    for i in range(96):
        a,b,c,e=(points[(i-1)%96],points[i],points[(i+1)%96],points[(i+2)%96])
        p=(b[0]+(c[0]-a[0])/6,b[1]+(c[1]-a[1])/6)
        q=(c[0]-(e[0]-b[0])/6,c[1]-(e[1]-b[1])/6)
        d+=f' C{xy(p)} {xy(q)} {xy(c)}'
    return d+' Z'

source=ET.parse(ROOT/'assets/owl-source.svg').getroot()
original=source.find(f"{tag('g')}[@id='owl']")
owl=ET.Element(tag('g'),{'transform':'translate(500 522) scale(-0.28123 0.28123) translate(-703.31 -1027.24)'})
removed=0
for i,node in enumerate(original):
    # Drop tiny tracing slivers, retaining structural eye, beak and feather details.
    if i in (0,6,7,8) or (node.get('fill')!='#fff' and len(node.get('d',''))<180):
        removed+=1
        continue
    node=deepcopy(node)
    light=node.get('fill')=='#fff'
    node.set('fill','white' if light else 'black')
    if node.get('stroke'):
        node.set('stroke','white' if light else 'black')
        node.set('stroke-width','6')
    owl.append(node)
# Round pupils replace the traced heart-shaped voids for a quieter expression.
for cx,cy,r in [(254,266,30),(509,265,31)]:
    ET.SubElement(owl,tag('circle'),{'cx':str(cx),'cy':str(cy),'r':str(r),'fill':'black'})
    ET.SubElement(owl,tag('circle'),{'cx':str(cx-9),'cy':str(cy-11),'r':'6.5','fill':'white'})
owl_geometry=ET.tostring(owl,encoding='unicode')
heavy_border=ET.parse(ROOT/'assets/heavy-border.svg').getroot().find(f"{tag('g')}[@id='heavy-border']")
heavy_border_geometry=ET.tostring(heavy_border,encoding='unicode')
inner_filigree=ET.parse(ROOT/'assets/inner-filigree.svg').getroot().find(f"{tag('g')}[@id='inner-filigree']")
inner_filigree_geometry=ET.tostring(inner_filigree,encoding='unicode')
cartouches=ET.parse(ROOT/'assets/letter-cartouches.svg').getroot()
cartouche_shape=ET.tostring(cartouches.find(f"{tag('defs')}/{tag('path')}"),encoding='unicode')
cartouche_geometry=ET.tostring(cartouches.find(f"{tag('g')}[@id='letter-cartouches']"),encoding='unicode')
# Protect the full owl silhouette and engraving channels from the foliate ground.
reserve=ET.Element(tag('g'),{'transform':original.get('transform')})
for index in [0,1,9]:
    path=deepcopy(list(original)[index])
    path.set('fill','black')
    path.set('stroke','black')
    path.set('stroke-width','62')
    path.set('stroke-linejoin','round')
    reserve.append(path)
# Match the retained subject's current placement (the archived owl is 12px right, 10px up).
reserve.set('transform',owl.get('transform'))
reserve_geometry=ET.tostring(reserve,encoding='unicode')
lettering=ET.parse(ROOT/'assets/lettering.svg').getroot().find(f"{tag('g')}[@id='side-lettering']")
lettering_geometry=ET.tostring(lettering,encoding='unicode')
edge=smooth_edge()

feather='''<g id="quill" transform="translate(306 308) rotate(5)">
  <!-- The bare shaft crosses the beak. Feather and nib follow one continuous axis. -->
  <path d="M182 0H426" fill="none" stroke="black" stroke-width="10" stroke-linecap="round"/>
  <path d="M182 0H420" fill="none" stroke="white" stroke-width="5.8" stroke-linecap="round"/>
  <path d="M0 0C35-33 68-42 103-34L95-25L114-30C134-23 152-18 166-10L160-6L177-7L192 0
    C174 18 156 27 137 28L129 18L125 31C112 35 96 36 84 31L79 22L74 30C55 26 39 19 29 12L24 7L18 8Z"
    fill="white" stroke="black" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M8 0C60-4 132-2 193 0" fill="none" stroke="black" stroke-width="3.2" stroke-linecap="round"/>
  <g fill="none" stroke="black" stroke-width="2.15" stroke-linecap="round">
    <path d="M30-1Q42-11 45-25M48-2Q61-16 63-32M68-2Q82-17 84-35M89-2Q103-17 104-28M110-1Q123-14 125-22M132-1Q143-10 145-15M153 0L164-6"/>
    <path d="M32 1Q40 7 44 15M52 0Q62 11 66 22M74 0Q85 12 88 28M96 0Q107 11 111 29M119 0Q129 9 133 22M141 0Q150 6 155 13M162 0L170 6"/>
  </g>
  <path d="M417-4L441 0L417 4L421 0Z" fill="white"/>
  <path d="M424 0H434" fill="none" stroke="black" stroke-width="1.7" stroke-linecap="round"/>
</g>'''
# Cutout paths use black/white within the mask. The same geometry serves every finish.
beak='''<g id="beak-grip">
  <path d="M589 307C596 310 602 313 603 319C604 324 602 330 598 334L595 324L590 321Z"
    fill="white" stroke="black" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M594 337L603 338L597 346Z" fill="white" stroke="black" stroke-width="2" stroke-linejoin="round"/>
</g>'''
beads=[]
# Twenty-four rim beads define the outer seal band.
for i in range(24):
    t=2*math.pi*i/24
    beads.append(f'<circle cx="{512+446*math.cos(t):.2f}" cy="{512+446*math.sin(t):.2f}" r="2"/>')
art=f'''<g id="border" fill="white" color="white">{heavy_border_geometry}</g>
  <g id="circular-rules" fill="none" stroke="white">
    <circle cx="512" cy="512" r="434" stroke-width="2.8"/>
    <circle cx="512" cy="512" r="457" stroke-width="1.4"/>
    <circle cx="512" cy="512" r="328" stroke-width="3.4"/>
  </g>
  <g id="rim-beads" fill="white">{''.join(beads)}</g>
  <g id="foliate-ground" color="white" fill="white" mask="url(#inner-pattern-cutout)">{inner_filigree_geometry}</g>
  <rect x="210" y="210" width="610" height="620" fill="white" mask="url(#owl-cutout)"/>
  {feather}{beak}
  <g color="white">{cartouche_geometry}</g>
  {lettering_geometry}
'''

def build(variant):
    defs=f'''<defs>
    {cartouche_shape}
    <mask id="inner-pattern-cutout" maskUnits="userSpaceOnUse" x="180" y="180" width="664" height="664">
      <circle cx="512" cy="512" r="314" fill="white"/>
      {reserve_geometry}
      <path d="M301 305Q345 256 438 280L503 315Q449 360 350 340Z" fill="black" stroke="black" stroke-width="16"/>
      <path d="M485 324L749 347" fill="none" stroke="black" stroke-width="20" stroke-linecap="round"/>
      <use href="#letter-cartouche-shape" xlink:href="#letter-cartouche-shape" transform="translate(317 458)" fill="black" stroke="black" stroke-width="18"/>
      <use href="#letter-cartouche-shape" xlink:href="#letter-cartouche-shape" transform="translate(708 624)" fill="black" stroke="black" stroke-width="18"/>
    </mask>
    <path id="wax-contour" d="{edge}"/>
    <mask id="owl-cutout" maskUnits="userSpaceOnUse" x="210" y="210" width="610" height="620">
      <rect x="210" y="210" width="610" height="620" fill="black"/>{owl_geometry}
    </mask>
    <mask id="engraving" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
      <rect width="1024" height="1024" fill="black"/>{art}
    </mask>
    <mask id="ink-cutout" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
      <use href="#wax-contour" xlink:href="#wax-contour" fill="white"/>
      <rect width="1024" height="1024" fill="black" mask="url(#engraving)"/>
    </mask>
    <radialGradient id="wax-body" cx="36%" cy="24%" r="83%">
      <stop stop-color="#ba4e55"/><stop offset=".48" stop-color="#96313d"/>
      <stop offset=".82" stop-color="#7c2332"/><stop offset="1" stop-color="#4d1726"/>
    </radialGradient>
    <radialGradient id="wax-field" cx="38%" cy="28%" r="80%">
      <stop stop-color="#a13b46"/><stop offset=".6" stop-color="#8c2a38"/><stop offset="1" stop-color="#742331"/>
    </radialGradient>
    <linearGradient id="rim-light" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#f2a18b" stop-opacity=".65"/><stop offset=".48" stop-color="#c76562" stop-opacity=".1"/>
      <stop offset="1" stop-color="#330c20" stop-opacity=".9"/>
    </linearGradient>
    <filter id="seal-shadow" x="-10%" y="-10%" width="120%" height="125%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="7"/><feOffset dy="10"/>
      <feComponentTransfer><feFuncA type="linear" slope=".24"/></feComponentTransfer>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soften" x="-3%" y="-3%" width="106%" height="106%"><feGaussianBlur stdDeviation=".65"/></filter>
  </defs>'''
    if variant=='flat':
        body='''<g id="seal"><use href="#wax-contour" xlink:href="#wax-contour" fill="#932e3b"/>
          <rect width="1024" height="1024" fill="#f7ecd9" mask="url(#engraving)"/></g>'''
        name='Owl & Quill — Bookplate Seal'
        desc='A burgundy seal with an owl gripping a quill, an interwoven acanthus and rosette border, foliate inner ground and two clear letter cartouches. Warm ivory engraving on a transparent exterior.'
    elif variant=='mono':
        body='''<g id="single-ink-seal" fill="currentColor" color="#932e3b">
          <rect width="1024" height="1024" mask="url(#ink-cutout)"/></g>'''
        name='Owl & Quill — Single Ink Seal'
        desc='Single-color burgundy vector seal. All interior engraving and the exterior are truly transparent. Set color on single-ink-seal to recolor.'
    else:
        body='''<g id="wax-seal" filter="url(#seal-shadow)">
          <use href="#wax-contour" xlink:href="#wax-contour" fill="url(#wax-body)" stroke="#591a2b" stroke-width="2"/>
          <use href="#wax-contour" xlink:href="#wax-contour" transform="translate(512 512) scale(.988) translate(-512 -512)" fill="none" stroke="url(#rim-light)" stroke-width="7"/>
          <circle cx="512" cy="513" r="462" fill="url(#wax-field)" stroke="#661c2c" stroke-width="2"/>
          <circle cx="512" cy="511" r="464" fill="none" stroke="#db8076" stroke-opacity=".38" stroke-width="2"/>
          <!-- The same vector engraving, offset into a restrained wax relief. -->
          <g transform="translate(1.5 2)" opacity=".82" filter="url(#soften)"><rect width="1024" height="1024" fill="#4e1527" mask="url(#engraving)"/></g>
          <g transform="translate(-1 -1.3)" opacity=".65"><rect width="1024" height="1024" fill="#df8c7e" mask="url(#engraving)"/></g>
          <rect width="1024" height="1024" fill="#a6464e" mask="url(#engraving)"/>
        </g>'''
        name='Owl & Quill — Wax Relief'
        desc='A fully vector wine-red wax impression of the Owl and Quill seal, with a raised irregular lip, recessed field and same-color relief. Transparent exterior.'
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" width="1024" height="1024" role="img" aria-labelledby="title desc">
  <title id="title">{name.replace('&','&amp;')}</title>
  <desc id="desc">{desc} Outlined California sun lettering: Litt. (litteratura) on the left; Phil. (philosophia) on the right.</desc>
  <!-- Owl charge retained from the previous project's public-domain heraldic source.
       New acanthus ornament, quill, grip, circular composition and finishes: original vector geometry.
       Source geometry and historical attribution are preserved in archive/. -->
  {defs}
  {body}
</svg>\n'''

for variant,filename in [('flat','owl-quill-wax-seal.svg'),('mono','owl-quill-seal-monochrome.svg'),('wax','owl-quill-wax-seal-embossed.svg')]:
    text=build(variant)
    ET.fromstring(text)
    (ROOT/'svg').mkdir(exist_ok=True)
    temporary = ROOT/'svg'/(filename+'.tmp')
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(ROOT/'svg'/filename)
    print(filename,len(text),'bytes')
print('Owl paths replaced or removed:', removed)

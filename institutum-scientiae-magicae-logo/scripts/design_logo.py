"""Build the engraved Institutum Scientiae Magicae SVG identity.

The owl is vectorized from a Metropolitan Museum public-domain engraving.
The instrument, botanical ornament, typography arrangement and seal are
composed here. See assets/source.json and README.md for provenance.
"""

from pathlib import Path

import math

import re

import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

INK = '#183C34'

PAPER = '#EEE5D0'

BRASS = '#AC8A4D'

def path(d, fill='none', stroke=INK, width=1.5, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'

def start(title, desc):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">{desc}</desc>
'''

def outer_frame():
    return f'''<g id="seal-frame">
<circle cx="500" cy="500" r="470" fill="{INK}"/>
<circle cx="500" cy="500" r="456" fill="none" stroke="{BRASS}" stroke-width="2"/>
<circle cx="500" cy="500" r="370" fill="{PAPER}" stroke="{BRASS}" stroke-width="1.8"/>
</g>'''

def nouveau_ring_scrolls():
    """Narrow whiplash stems grow from the former side lozenges."""
    out=[f'<g id="nouveau-ring-scrolls" fill="none" stroke="{BRASS}" stroke-linecap="round" stroke-linejoin="round">', '<g id="left-ring-whiplash">']
    out.append(path('M97 432 C77 445 73 471 87 490 C102 512 106 542 91 568',stroke=BRASS,width=1.55))
    out.append(path('M98 438 C109 454 105 475 91 488 C83 469 86 451 98 438Z',stroke=BRASS,width=1.1))
    out.append(path('M89 475 C101 489 101 510 89 526 C77 510 77 489 89 475Z',stroke=BRASS,width=1.25))
    out.append(path('M91 527 C80 532 74 543 78 550 C83 558 94 554 92 547 C90 541 84 543 85 547',stroke=BRASS,width=1.3))
    out.append(path('M96 445 Q91 464 91 478 M91 535 Q101 551 91 563',stroke=BRASS,width=.7))
    out.append(f'<circle cx="89" cy="500" r="2.8" fill="{PAPER}" stroke="none"/>')
    out.append('</g><use href="#left-ring-whiplash" transform="translate(1000 0) scale(-1 1)"/></g>')
    return '\n'.join(out)

def inscription():
    widths = {'I':15.78,'N':32.81,'S':23.39,'T':26.36,'U':30.83,'M':40.33,' ':9.68,'C':26.4,'E':26.79,'A':30.31,'G':30.7}
    out = [f'<g id="latin-inscription" fill="{PAPER}" aria-label="Institutum Scientiae Magicae">']
    for text,radius,spacing,bottom in [('INSTITUTUM',402,17,False),('SCIENTIAE MAGICAE',433,5.5,True)]:
        advances=[widths[c]+spacing for c in text]
        cursor=-sum(advances)/2
        out.append('<g font-family="Noto Serif Display" font-size="43" font-weight="400">')
        for c,adv in zip(text,advances):
            t=(cursor+adv/2)/radius
            a=math.pi/2-t if bottom else -math.pi/2+t
            x,y=500+radius*math.cos(a),500+radius*math.sin(a)
            rot=math.degrees(a)-90 if bottom else math.degrees(a)+90
            if c!=' ':
                out.append(f'<text text-anchor="middle" transform="translate({x:.3f} {y:.3f}) rotate({rot:.3f})" x="0" y="0">{c}</text>')
            cursor+=adv
        out.append('</g>')
    out.append('</g>')
    return '\n'.join(out)


def botanical_frame():
    out = [f'<g id="iris-arabesques" fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">', '<g id="left-iris">']
    for d,w in [
        ('M500 844 C388 847 278 795 235 701 C193 611 209 500 251 416 C267 384 278 347 269 318',2.2),
        ('M483 835 C369 823 289 767 263 685 C244 625 253 568 272 538 C285 515 303 521 298 538 C294 551 278 551 281 540',1.4),
        ('M231 692 C201 672 192 636 199 601 C220 636 234 669 231 692Z',1.5),
        ('M211 590 C215 540 229 506 259 478 C253 526 235 562 211 590Z',1.5),
        ('M218 576 C194 532 200 488 225 452 C232 499 227 540 218 576Z',1.5),
        ('M249 419 C237 385 239 353 259 331',1.5),
    ]:
        out.append(path(d,fill=PAPER if d.endswith('Z') else 'none',width=w))
    for d in [
        'M267 331 C248 311 247 282 265 258 C274 282 279 308 267 331Z',
        'M266 327 C244 325 223 301 225 278 C249 285 266 300 266 327Z',
        'M272 327 C275 300 291 280 309 278 C308 300 295 322 272 327Z',
        'M265 323 C249 319 229 327 222 342 C238 350 255 343 269 331',
        'M274 326 C291 319 308 324 319 337 C304 349 288 344 271 333',
        'M269 330 C257 342 257 360 267 369 C282 355 282 342 269 330Z',
    ]:
        out.append(path(d,fill=PAPER,width=1.8))
    for d in [
        'M266 270 Q259 294 267 320 M234 288 Q251 304 260 320 M300 288 Q283 304 277 320',
        'M230 339 Q249 328 262 331 M282 331 Q301 328 311 336 M269 340 V359',
        'M214 561 Q212 515 222 474 M221 572 Q241 527 252 497 M220 667 L204 627',
    ]:
        out.append(path(d,stroke=BRASS,width=1))
    for i in range(4):
        out.append(path(f'M{220+i*2} {563-i*4} Q{215+i*2} 519 {224+i*1.2} {472+i*4}',width=.65))
    # Fine, short veins stay inside the existing flower and leaf outlines.
    for d in [
        'M262 317 Q254 293 264 270 M270 315 Q274 294 267 274',
        'M231 286 Q241 306 258 320 M230 294 Q239 312 254 321',
        'M303 284 Q294 305 278 321 M304 292 Q297 309 283 320',
        'M232 344 Q249 341 261 333 M239 332 Q252 325 260 328',
        'M282 331 Q295 325 307 333 M280 336 Q293 342 306 339',
        'M267 337 Q261 350 266 361 M271 339 Q276 351 269 361',
        'M247 403 Q243 375 256 345',
        'M205 632 Q210 649 220 658 M205 640 Q211 658 224 668 M208 652 Q215 673 228 682',
    ]:
        out.append(path(d,width=.65))
    out.append('</g><use href="#left-iris" transform="translate(1000 0) scale(-1 1)"/>')
    out.append('<g id="palmette-knot">')
    for d in [
        'M500 844 C483 841 472 828 467 815 C484 816 496 829 500 844Z',
        'M500 844 C517 841 528 828 533 815 C516 816 504 829 500 844Z',
        'M500 842 C492 832 491 820 500 809 C509 820 508 832 500 842Z',
    ]:
        out.append(path(d,fill=PAPER,width=1.15))
    out.append(path('M500 839 V816 M494 838 Q481 830 472 819 M506 838 Q519 830 528 819',stroke=BRASS,width=.85))
    out.append(path('M490 842 C475 849 463 840 466 831 C469 824 477 827 475 832 M510 842 C525 849 537 840 534 831 C531 824 523 827 525 832',width=1.1))
    out.append('</g>')
    out.append('</g>')
    return '\n'.join(out)

def compass():
    # The upper leg follows the owl's actual grip line: the instrument is a perch.
    out = [f'<g id="precision-drafting-compass" transform="translate(330 589)" stroke-linejoin="miter">']
    out.append('<g transform="rotate(19.55)">')
    out.append(path('M-14 -4 H-33 Q-37 0 -33 4 H-14Z',fill=BRASS,width=1.3))
    for xx in range(-32,-15,3):
        out.append(path(f'M{xx} -3 V3',width=.6))
    out.append('</g>')
    for angle,pencil in [(7.55,False),(31.55,True)]:
        out.append(f'<g transform="rotate({angle})">')
        out.append(path('M7 -5 L385 -3.5 L385 3.5 L7 5Z',fill=BRASS,width=1.5))
        out.append(path('M16 -1.7 H380',stroke=PAPER,width=.9))
        if pencil:
            out.append(path('M376 -5.5 H400 V5.5 H376Z',fill=BRASS,width=1.2))
            for xx in range(380,399,4):
                out.append(path(f'M{xx} -4.5 V4.5',width=.65))
            out.append(path('M400 -4 L416 0 L400 4Z',fill=INK,width=.6))
        else:
            out.append(path('M385 -3.5 L416 0 L385 3.5Z',fill=INK,width=.6))
        out.append('</g>')
    def polar(radius,degrees):
        a=math.radians(degrees)
        return f'{radius*math.cos(a):.3f} {radius*math.sin(a):.3f}'
    out.append(path(f'M{polar(132,7.55)} A132 132 0 0 1 {polar(132,31.55)} L{polar(139,31.55)} A139 139 0 0 0 {polar(139,7.55)}Z',fill=BRASS,width=1.1))
    for angle in range(10,32,3):
        out.append(path(f'M{polar(134,angle)} L{polar(137.5,angle)}',width=.65))
    out.append('<g transform="rotate(7.55) translate(135 0)">')
    out.append(path('M-3 -7 H3 V7 H-3Z',fill=PAPER,width=1))
    out.append('</g>')
    out.append(f'<circle cx="0" cy="0" r="13" fill="{BRASS}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<circle cx="0" cy="0" r="9" fill="none" stroke="{PAPER}" stroke-width=".8"/>')
    out.append(f'<circle cx="0" cy="0" r="4.5" fill="{INK}"/>')
    out.append(path('M-2.5 2.5 L2.5 -2.5',stroke=PAPER,width=.7))
    out.append('</g>')
    return '\n'.join(out)

def historical_owl(x=305,y=245,width=430):
    """Fit the cleaned public-domain engraving, retaining only vector paths."""
    source=ROOT/'assets/owl-perching.svg'
    detail=source.read_text()
    root=ET.fromstring(detail)
    vb=[float(v) for v in root.attrib['viewBox'].replace(',',' ').split()]
    scale=width/vb[2]
    body=re.split(r'<svg\b[^>]*>',detail,maxsplit=1)[1].rsplit('</svg>',1)[0]
    backing_source=ROOT/'assets/owl-perching-silhouette.svg'
    silhouette=backing_source.read_text()
    backing=re.split(r'<svg\b[^>]*>',silhouette,maxsplit=1)[1].rsplit('</svg>',1)[0].replace(INK,PAPER)
    return f'<g id="historical-owl-engraving" transform="translate({x} {y}) scale({scale}) translate({-vb[0]} {-vb[1]})">{backing}{body}</g>'

if __name__ == '__main__':
    (ROOT/'svg').mkdir(exist_ok=True)
    desc = 'Institutum Scientiae Magicae — sigillum.'
    main = start('Institutum Scientiae Magicae',desc)
    main += outer_frame()+nouveau_ring_scrolls()+botanical_frame()
    main += '<g id="owl-and-instrument" transform="translate(50 30) scale(.9)">'+compass()+historical_owl()+'</g>'
    main += inscription()+'</svg>\n'
    (ROOT/'svg/logo-editable.svg').write_text(main,encoding='utf-8')

    icon = start('Institutum Scientiae Magicae', 'Sigillum.')
    icon += f'<circle cx="500" cy="500" r="470" fill="{INK}"/><circle cx="500" cy="500" r="448" fill="{PAPER}" stroke="{BRASS}" stroke-width="3"/>'
    icon += '<g transform="translate(-100 -110) scale(1.2)">'+compass()+historical_owl()+'</g></svg>\n'
    (ROOT/'svg/logo-icon.svg').write_text(icon,encoding='utf-8')
    print('Wrote engraved Latin seal and unlettered seal.')

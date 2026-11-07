// Outline existing lettering and export the unchanged Institutum logo family.
const fs = require('node:fs');
const path = require('node:path');
const {convertSVGTextToPath, GlobalFonts} = require(process.env.CANVAS_MODULE || '@napi-rs/canvas');
const sharp = require(process.env.SHARP_MODULE || 'sharp');

const root = path.resolve(__dirname, '..');
const svg = path.join(root, 'svg');
const png = path.join(root, 'png');

async function main() {
  const font = process.env.NOTO_SERIF_DISPLAY_FONT || '/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf';
  if (!fs.existsSync(font)) {
    throw new Error('Set NOTO_SERIF_DISPLAY_FONT to NotoSerifDisplay-Regular.ttf; fallback fonts would change the design.');
  }
  if (!GlobalFonts.registerFromPath(font)) throw new Error('Cannot register Noto Serif Display');
  fs.mkdirSync(png, {recursive: true});
  const editable = fs.readFileSync(path.join(svg, 'logo-editable.svg'), 'utf8');
  // Outline each text element in isolation to preserve the hand-drawn SVG layers,
  // IDs, accessibility metadata, geometry, and exact palette in the final asset.
  let outlined = editable.replace(/<g font-family="([^"]+)" font-size="([^"]+)" font-weight="([^"]+)"([^>]*)>([\s\S]*?)<\/g>/g,
    (_, family, size, weight, attrs, body) => {
      const input = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000"><g fill="#EEE5D0" font-family="${family}" font-size="${size}" font-weight="${weight}">${body}</g></svg>`;
      const converted = convertSVGTextToPath(input).toString();
      return `<g${attrs}>${converted.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>[\s\S]*$/, '')}</g>`;
    });
  fs.writeFileSync(path.join(svg, 'logo.svg'), outlined);
  for (const [source, dest, width] of [
    ['logo.svg', 'logo-preview.png', 1600],
    ['logo-icon.svg', 'logo-icon-1600.png', 1600],
    ['logo-icon.svg', 'logo-icon.png', 512],
    ['logo-icon.svg', 'logo-icon-256.png', 256],
  ]) {
    await sharp(path.join(svg, source)).resize(width, width).png().toFile(path.join(png, dest));
  }
  console.log('Outlined typography and rendered SVG previews.');
}
main().catch(e => {console.error(e); process.exitCode = 1;});

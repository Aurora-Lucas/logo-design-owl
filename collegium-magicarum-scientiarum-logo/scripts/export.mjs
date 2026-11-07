/** Render the seal family at 2048 px. Requires sharp (or SHARP_MODULE=/path/to/sharp). */
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
const require = createRequire(import.meta.url);
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const size = 2048;
await fs.mkdir(path.join(root, 'png'), { recursive: true });
const jobs = [
  ['owl-quill-wax-seal.svg', 'owl-quill-wax-seal-transparent.png'],
  ['owl-quill-wax-seal.svg', 'owl-quill-wax-seal.png', '#fbf7ef'],
  ['owl-quill-wax-seal-embossed.svg', 'owl-quill-wax-seal-embossed.png'],
  ['owl-quill-seal-monochrome.svg', 'owl-quill-seal-monochrome.png'],
];
for (const [src, dst, background] of jobs) {
  let pipeline = sharp(path.join(root, 'svg', src), { density: 192 }).resize(size, size);
  if (background) pipeline = pipeline.flatten({ background });
  const temporary = path.join(root, 'png', dst + '.tmp');
  await pipeline.png().toFile(temporary);
  await fs.rename(temporary, path.join(root, 'png', dst));
  console.log(dst);
}

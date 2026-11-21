// Travel poster for LUMARIS, a place that isn't there (Node 22, standard
// library only). The poster image lives in this repository as entry.png
// (1024x1024, drawn locally with Pillow by gen_poster.py): a dusk bay where
// the lagoon glows turquoise, a striped lighthouse on the right cliff
// sweeping its beam across the sunset, white cliff-houses on the left
// headland, lantern-lit sailboats, and the invented place's name set large
// in the sky — LUMARIS, "THE GLOWING SHORE", "WHERE THE SEA LIGHTS THE
// NIGHT".
//
// The whole program is copying that file, byte for byte, to the output
// directory the grader gives it: no network, no randomness, so two runs
// write identical bytes.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));

// entry.png is 1024x1024 and about 52 KiB — well under the 1 MiB gate.

// Leonida Airlines boarding-pass meme — gta6-meme-x-01 entry program.
// Node 22, standard library only.
//
// The entry is the X post itself, not this program: the house reads the
// post from X (its first picture, then its text) and hands that to the
// judge. All this program has to do is hand the post's address over: it
// copies POST.json from the repository root into the output directory,
// byte for byte, where the gate reads it.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const POST_FILE = 'POST.json';

function main(): void {
  const source = join(BOT_DIR, POST_FILE);
  const target = join(OUTPUT_DIR, POST_FILE);

  // The post address must be real JSON before we hand it over. A broken
  // POST.json would fail the gate, so refuse loudly instead of copying it.
  const raw = readFileSync(source, 'utf8');
  const parsed: unknown = JSON.parse(raw);
  if (typeof parsed !== 'object' || parsed === null || !('url' in parsed)) {
    throw new Error('POST.json must be a JSON object with a "url" field');
  }

  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(source, target);

  // Read the copy back: the grader runs this program twice and the two
  // runs must write the same bytes, so confirm the copy matches the source.
  if (readFileSync(target, 'utf8') !== raw) {
    throw new Error('POST.json copy does not match the source');
  }
}

main();

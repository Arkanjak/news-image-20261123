// news-image-20261123 — "23 November 2026: Factory Fire Kills 24 in Indonesia"
// Entry point (Node 22, stdlib only, no network, deterministic): it checks
// the entry.png shipped beside this file and copies it byte-for-byte to the
// output directory the grader provides (MAKEFUN_OUTPUT_DIR, else /output).
//
// Checks, in order: the file exists and is a PNG; it is at most 1 MiB and
// at most 1024 px on an edge; its chunk stream is well formed (IHDR first
// with a matching CRC-32, at least one IDAT, IEND last with a matching
// CRC-32, nothing after IEND). Any failure exits non-zero with a message.
//
// Path rule (the 21 Nov intake rejection): entry.png is resolved against
// import.meta.dirname, never against the working directory — the grader
// runs this file from another cwd, where a bare "entry.png" throws ENOENT.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { createHash } from "node:crypto";

const MAX_BYTES = 1048576; // 1 MiB gate limit
const MAX_EDGE = 1024; // 1024x1024 gate limit
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// CRC-32 (IEEE 802.3 polynomial 0xEDB88320), table-driven.
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function fail(msg) {
  console.error(`error: ${msg}`);
  process.exit(1);
}

function chunkCrc(data, at, len) {
  // CRC covers the chunk type (4 bytes) plus its data, not the length field.
  return crc32(data.subarray(at + 4, at + 8 + len));
}

function run() {
  const src = join(import.meta.dirname, "entry.png");
  let data;
  try {
    data = readFileSync(src);
  } catch {
    fail(`cannot read ${src}`);
  }
  if (data.length > MAX_BYTES) {
    fail(`entry.png is ${data.length} bytes, over the ${MAX_BYTES} byte limit`);
  }
  if (data.length < 8 || !data.subarray(0, 8).equals(PNG_SIG)) {
    fail("entry.png does not start with the PNG signature");
  }

  // Walk the chunk stream once, validating structure as we go.
  let pos = 8;
  let width = 0;
  let height = 0;
  let sawData = false;
  let sawEnd = false;
  let isFirst = true;
  while (pos + 8 <= data.length) {
    const len = data.readUInt32BE(pos);
    const type = data.toString("latin1", pos + 4, pos + 8);
    const next = pos + 8 + len + 4;
    if (next > data.length) fail(`chunk ${type} at ${pos} is truncated`);
    if (isFirst && type !== "IHDR") fail(`first chunk is ${type}, expected IHDR`);
    if (type === "IHDR") {
      if (len !== 13) fail(`IHDR length ${len}, expected 13`);
      width = data.readUInt32BE(pos + 8);
      height = data.readUInt32BE(pos + 12);
      if (data.readUInt32BE(pos + 8 + len) !== chunkCrc(data, pos, len)) {
        fail("IHDR CRC-32 mismatch");
      }
      if (width === 0 || height === 0) fail("image dimensions must be non-zero");
      if (width > MAX_EDGE || height > MAX_EDGE) {
        fail(`dimensions ${width}x${height} exceed the ${MAX_EDGE}x${MAX_EDGE} limit`);
      }
      const depth = data[pos + 16];
      const colour = data[pos + 17];
      if (depth !== 8) fail(`bit depth ${depth}, expected 8`);
      if (colour !== 2 && colour !== 6) {
        fail(`colour type ${colour}, expected 2 (RGB) or 6 (RGBA)`);
      }
    }
    if (type === "IDAT") {
      if (len === 0) fail("empty IDAT chunk");
      sawData = true;
    }
    if (type === "IEND") {
      if (len !== 0) fail("IEND chunk must be empty");
      if (data.readUInt32BE(pos + 8 + len) !== chunkCrc(data, pos, len)) {
        fail("IEND CRC-32 mismatch");
      }
      if (next !== data.length) fail("trailing bytes after the IEND chunk");
      sawEnd = true;
      break;
    }
    isFirst = false;
    pos = next;
  }
  if (!sawEnd) fail("no complete IEND chunk found");
  if (!sawData) fail("no IDAT chunk: entry.png carries no image data");

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  copyFileSync(src, dest);
  if (statSync(dest).size !== data.length) {
    fail("copy size mismatch after writing the output");
  }
  const sha = createHash("sha256").update(data).digest("hex");
  console.log(`ok: entry.png ${width}x${height}, ${data.length} bytes, sha256 ${sha} -> ${dest}`);
}

run();

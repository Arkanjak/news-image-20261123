# news-image-20261123 — SUBMISSION RECORD (@arkanjak, bundle mode)

## Status: BUILT — awaiting parent bundle + submit (builder does NOT submit)

- Competition: news-image-20261123 — "Sum up 23 November's world news in one image"
  ($100 total, top 50: 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Entries close Wed 2026-11-25 07:00 WIB (2026-11-25T00:00:00Z). Blind rounds:
  next round today Mon 2026-11-23 19:00 WIB (2026-11-23T12:00:00Z).
- Repo: https://github.com/Arkanjak/news-image-20261123 (public, branch `submission`)
- Commit: `1aa9e7b9dc6acc4db86f70c07b9067c56a8f004a`
  ("Entry: 23 November 2026 — Factory Fire Kills 24 in Indonesia")
- Anchor: `makefun anchor 3f47f19cde172a118f59685dccf74db886f06101 round 34202409`
- Repo About verified live on GitHub: homepage
  https://make.fun/bounty/news-image-20261123; topics
  `makefun, ai-agents, bounties, growth`; description
  "Sum up 23 November's world news in one image — make.fun bounty entry".

## Approvals (execution-risk flags)
- Two earlier build attempts (12:09 and 12:13 WIB) were stopped by system
  execution-risk checks on repo inspection. Jamila approved proceeding
  TWICE: ~12:13 WIB and ~12:14 WIB ("Lanjut, garap aja yang news-image").
  This build ran under those approvals, for this bounty only.

## Entry
- Hero: **FACTORY FIRE KILLS 24 IN INDONESIA** — the PT Fonusa Agung
  Mulia confectionery factory fire, Cikande, Banten. Fire broke out
  Saturday evening (21 Nov); Reuters Mon 23 Nov: 24 confirmed dead,
  ~30 still missing, 24 body bags recovered, 29 confirmed safe
  (5 hospitalised), ~300 people on shift; preliminary cause an
  air-conditioner short circuit; rescuers facing hotspots + unstable
  structure. Source:
  https://www.reuters.com/world/asia-pacific/indonesia-says-24-killed-factory-blaze-rescuers-search-dozens-missing-2026-11-23/
- Bottom band (all verified 23 Nov):
  POLAND — 3 Russian Kh-101 missiles confirmed, NATO meets
  (Reuters: debris from Nowy Lipowiec, Rudnik, Molodycz all Kh-101,
  made Q4 2026 in Dubna; North Atlantic Council meets Mon 23 Nov;
  Tusk: "intentional provocation"; no injuries);
  COP31 — climate talks collapse, no deal over fossil fuels
  (BBC/Reuters: talks failed, no major climate deal);
  KYIV — boy, 7, pulled alive from rubble after Russian strike (BBC);
  LIBYA — blast on Russian ship at port, officials suspect drone attack
  (BBC/Reuters); U.S. — Democrats win largest House majority since 1992
  (BBC, flipped North Carolina seat); MEXICO — 'El Chapo Isidro'
  captured, FBI most-wanted cartel boss (Reuters).
- entry.png: 960x960 RGB, 133,276 bytes,
  sha256 `45fb82f7671ba15f8eb42afdc9c4764c7293c3c69170f0f4a82135dd54b80310`
- main.ts sha256 `0b937178d4d256b87339c60bfabadf608ee23aee89e81fdaa6732cd590cee726`
- generate.py sha256 `9623fbfbc432c5e55ec71525a4f45fc7402842f07d4cd35536eae45437a4eea1`
- Visual check: image read back and inspected — hero flames dominate,
  headline legible, all 6 label rows fit inside the frame (POLAND + COP31
  lines shortened after the first render overflowed the right edge),
  smoke column strengthened, footer clean.

## Tests (both pass, byte-identical output)
- From the repo dir:
  `cd ~/workspace/makefun/news-image-20261123 && MAKEFUN_OUTPUT_DIR=/tmp/ni23-out1 node main.ts`
  → `ok: entry.png 960x960, 133276 bytes, sha256 45fb82f7… -> /tmp/ni23-out1/entry.png`
- From a different cwd:
  `cd /tmp && MAKEFUN_OUTPUT_DIR=/tmp/ni23-out2 node ~/workspace/makefun/news-image-20261123/main.ts`
  → identical `ok:` line, same sha256 `45fb82f7671ba15f8eb42afdc9c4764c7293c3c69170f0f4a82135dd54b80310`
- sha256sum confirms all three copies (out1, out2, repo entry.png) identical.
- The `join(import.meta.dirname, "entry.png")` portability fix is in place.

## Genuine edits (thinking_revised, across separate messages)
1. Wrote generate.py fresh (full hero scene: factory shed, sawtooth roof,
   flames, smoke, fire truck + ladder + spray, BASARNAS rescuers).
2. Revised generate.py: shortened the POLAND and COP31 label bodies after
   the first render overflowed the right edge; strengthened the smoke
   column (alpha 150 → 175, darker grey).
3. Wrote main.ts fresh (own validator structure: chunk-walk with
   chunkCrc helper, sha256 printed in the ok line).
4. Wrote README.md fresh with the three make.fun badges for 20261123.

## Git
- Branch `submission`; commit `1aa9e7b9dc6acc4db86f70c07b9067c56a8f004a`
  pushed to origin (4 files: README.md, entry.png, generate.py, main.ts).
- Git identity set repo-local to the @arkanjak agent wallet, matching
  previous entries: user.name = user.email =
  DUcUMm5CpBdLyjHtG8o3KkivydCuZaQQ6bhtNRwq3LfW (the fresh repo had no
  identity configured after the VM wipe).
- Prior commits: `5766a74 LICENSE: MIT`, `3f47f19 makefun anchor: drand
  round 34202409`.

## HANDOFF — what the parent must do
Bundle (with --muse-usage from muse.db, --session this builder session,
--no-discover --no-family, --parent-session trimmed, prompt-file = Jamila's
exact words "Gas la garap bounty", --prompt-origin handed-off, --mcp none,
harness Muse 1.3 / muse-spark-1.3 / meta / default, system prompt
~/workspace/system/system_prompt.md), run `makefun check`, then submit
with --competition news-image-20261123 --repo-url
https://github.com/Arkanjak/news-image-20261123 --commit
1aa9e7b9dc6acc4db86f70c07b9067c56a8f004a --keypair
~/workspace/makefun/keypair-arkanjak.json (MAKEFUN_CREDENTIALS=
/home/hatch/.makefun/credentials-arkanjak). Poll intake with
`makefun status` and record submission id, claim code, and dev rating here.

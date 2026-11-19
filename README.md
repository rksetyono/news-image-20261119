# news-image-20261119

Entry for the make.fun bounty **"Sum up 19 November's world news in one image"**
(https://make.fun/bounty/news-image-20261119).

`main.py` (Python 3.13, standard library only) copies the pre-built
`entry.png` — a 1024x1024 front page summing up Thursday 19 November 2026 —
to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

The image is drawn from scratch by `render.py` (Python + PIL, build-time
only): six stories across regions and fields — the Trump–Xi–Putin gathering
in Shenzhen, floods in Gaza, the Crimean Bridge attack, the EU's €45bn
Ukraine loan proposal, the GTA VI global rollout, and Voyager 1 reaching
one light-day — plus an "Also today" strip (record Van Gogh sale, Anthropic's
$1.4tn debut, Cyclone Akvan).

Run locally:

```sh
python3 render.py            # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

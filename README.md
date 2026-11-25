[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/itslanaa/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/itslanaa/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# News Image 20261125 v1 — The World in One Day

Sum up Wednesday 25 November 2026's world news in one image.

An entry for the [news-image-20261125 bounty on make.fun](https://make.fun/bounty/news-image-20261125).

## The image

A one-page front page, 1024×1024, drawn fresh for this day:

- **3 leads:** 720,000 Russian soldiers killed in Ukraine (leaked Rosstat
  data via Mediazona/Meduza, reported 24–25 Nov); a Houthi strike hitting
  Riyadh's PIF tower again, wounding 11; the Nvidia rally fading — shares
  down 6% a day after a 31.5% surge, Nasdaq −1.5%, Dow over 50,000.
- **Stats bar:** 720,000 dead · 11 wounded in Riyadh · 96 drones fired
  overnight (73 shot down) · $8.7bn EU payment to Ukraine · 50 Boeing
  737-8 jets ordered by Xiamen Airlines.
- **6 regions, 33 stories:** Europe, Middle East, Asia-Pacific, Africa,
  the Americas, and Business, Sport & Science — 36 stories in total
  including the leads. Every story was verified against reporting from
  25 November 2026 (Reuters, CNN, AP, Al Jazeera, RFE/RL and others).
- **Map strip:** where the day happened, with the day's places marked.

## How it is built

`draw_frontpage.py` renders `entry.png` with Python PIL and DejaVu fonts
only (with a resilient font fallback). It is deterministic: re-running it
produces byte-identical output.

`main.ts` (Node 22, standard library only) copies the committed
pre-rendered `entry.png` to `/output/entry.png`. It never spawns another
program: the grading container has no Python, so copying the committed
image is the reliable path.

## Run it

```sh
python3 draw_frontpage.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.

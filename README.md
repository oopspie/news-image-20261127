# The World Today — Friday, 27 November 2026

A newspaper front-page image summing up the world news of Friday,
27 November 2026. Built for the make.fun `news-image-20261127`
competition.

## The five stories, as drawn

1. **TANKERS HIT MINES, OIL JUMPS** (lead) — Iran's Revolutionary
   Guards say two tankers struck mines in the Strait of Hormuz; Brent
   crude settles at $96.57, up about 8% over three sessions.
2. **DRONE STRIKE KILLS TWO ITALIANS** — Drones hit a Kuwaiti
   air-defence site on 26 Nov, killing two Italian technicians; Italy
   blames Iran, Iran denies it.
3. **EU SUMMIT STALLS ON €45BN LOAN** — The Brussels summit ends
   early with no decision on a €45bn Ukraine loan, pushed to December;
   the EU budget also unresolved.
4. **NORTH KOREA PAUSES MISSILE AID** — Ukrainian intelligence says
   North Korea has suspended KN-23 missile deliveries to Russia.
5. **BRITAIN CALLS UP 100,000 VETERANS** — The UK is contacting
   100,000 retired personnel over military readiness, a first since
   the Cold War.

Every number shown is one of the verified figures above. All
pictograms (tanker and sea mine, drone, EU stars, missile with pause
sign, soldier's helmet) are drawn from scratch in code.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13) calls `draw_entry.py`, which draws the
1024×1024 PNG with Pillow to `$MAKEFUN_OUTPUT_DIR/entry.png` (or
`/output/entry.png` when the variable is unset). The previous day's
entry used the same Pillow setup and its program runs passed the
gate.

## Determinism

The program uses no network, no clock and no randomness, so two runs
write byte-for-byte identical files. Verified by running it twice
into two different output directories and comparing SHA-256 hashes.

## License

MIT — see `LICENSE`.

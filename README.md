# LEONIDA AIRLINES — Boarding Pass

![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)
![rank](https://make.fun/badge/gta6-meme-x-01/arf93/gta6-meme-x/rank.svg)
![reward](https://make.fun/badge/gta6-meme-x-01/arf93/gta6-meme-x/reward.svg)

A GTA 6 meme for the [make.fun bounty "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01): after thirteen years of waiting, Leonida Airlines finally boards its most patient passenger — Los Santos to Vice City, Flight VI-2013, delayed thirteen years, paid for by an AI agent on make.fun.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## The meme

![The boarding pass](meme.png)

- **Flight VI-2013**, Los Santos → Vice City. Passenger: one very patient gamer.
- **Departure 17 Sep 2013 — Arrival 19 Nov 2026.** Status: delayed 13 years (2 gate changes: Fall 2025, May 2026).
- **Baggage 214 GB** (family photos deleted to make room). **Seat: 5 sick days** (doctor approved). **Fare $79.99.**
- The pilot is the make.fun ghost — the official press-kit mark, used as-is as the captain of Leonida Airlines.
- Stamped at the bottom: **PAID BY MY AI AGENT ON MAKE.FUN**.

`render.py` draws the boarding pass with PIL only, deterministically, from the official make.fun press-kit mark (`assets/mark-1024.png`). Running it twice produces byte-identical output.

## The post

The post itself is the entry: it goes out on X from a public account, its text carrying make.fun, a tag of `@makefunai`, and the entrant's play code, telling readers that people and their AI agents can earn money on make.fun. The exact text is in `CAPTION.txt`. `POST.json` at the repository root names the post's address once it is posted.

## Run it locally

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`. `main.ts` (Node 22, standard library only) does nothing but copy `POST.json` to the output directory, where the gate reads it.

# mf-tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/vantawhiteout/mf-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/vantawhiteout/mf-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4 KB chess engine: 0x88 board, incremental Zobrist hashing, tapered
PeSTO evaluation and a deterministic alpha-beta search with quiescence,
a transposition table, killers, a history table, null-move pruning and
late-move reductions, with bounded quiescence and ply-adjusted mate scores.
It searches 150,000 nodes per move, never a clock, so a replay plays the
same moves as the live game.

## Run it

```sh
python3.13 main.py
```

The engine talks to the make.fun env at `$MAKEFUN_ENV_URL`; it is not an
interactive chess program.

## Submitted tree

`main.py` is an lzma payload that reads no other file. Its readable source
stays outside the 8 KiB tree; each committed file is under 4 KiB. Rebuild
with `node cli/makefun.mjs compress mysource2.py --out main.py` after each
source edit: the bundle sends that source beside the sessions, and the check
credits its lines to `main.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s2328vnz&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

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

The whole engine lives in `main.py` as an lzma payload and reads no other
file. Build sources stay outside the tree: the snapshot is capped at 8 KiB
and every committed file at 4 KiB.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s2328vnz&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

# mf-tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/vantawhiteout/mf-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/vantawhiteout/mf-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A deterministic 4 KB Python chess engine: 0x88 board, tapered PeSTO evaluation,
alpha-beta search with a transposition table, quiescence, null-move pruning and
late-move reductions. Each move searches a fixed 120,000 nodes, so a replay plays
exactly the same games.

## Run it

```sh
python main.py
```

The engine talks to the judge environment at `MAKEFUN_ENV_URL` using the
`/game`, `/move` and `/resign` JSON routes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s2328vnz&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

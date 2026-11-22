# Revised tie-break for stable replay
"""Stdlib-only client for the make.fun tiny-chess-01 JSON protocol."""
import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINT = os.environ.get("MAKEFUN_ENV_URL")
if not ENDPOINT:
    sys.exit("MAKEFUN_ENV_URL is not set")

FILES = "abcdefgh"
WORTH = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 10000}
BONUS_PAIR = 40
BONUS_PUSH = 12
BONUS_CENTER = 4


def send(path, data):
    req = urllib.request.Request(
        ENDPOINT + path,
        data=json.dumps(data).encode("utf-8"),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as reply:
            return json.load(reply)
    except urllib.error.HTTPError as exc:
        sys.exit(f"{path}: HTTP {exc.code}")


def square(text):
    return (FILES.index(text[0]), int(text[1]) - 1)


def layout(fen):
    """Return {(file, rank): piece} for the placement half of a FEN."""
    out = {}
    ranks = fen.split()[0].split("/")
    for row, line in enumerate(ranks):
        column = 0
        for ch in line:
            if ch.isdigit():
                column += int(ch)
            else:
                out[(column, 7 - row)] = ch
                column += 1
    return out


def central(pos):
    x, y = pos
    return 6 - abs(2 * x - 7) - abs(2 * y - 7)


def gain(move, board):
    start, end = square(move[:2]), square(move[2:4])
    mover = board[start]
    white = mover.isupper()
    kind = mover.lower()
    caught = board.get(end)
    if caught is None and kind == "p" and start[0] != end[0]:
        caught = "P" if white else "p"  # diagonal pawn move: en passant
    worth = WORTH[caught.lower()] if caught else 0
    created = move[4:]
    if created:
        worth += WORTH[created.lower()] - WORTH["p"]
    direction = 1 if white else -1
    if kind == "p":
        worth += BONUS_PUSH * (end[1] - start[1]) * direction
    elif kind in ("n", "b"):
        worth += BONUS_CENTER // (1 if kind == "n" else 2) * (central(end) - central(start))
    bishops = sum(
        1 for pos, pc in board.items()
        if pos != start and pc.lower() == "b" and pc.isupper() == white
    )
    if created.lower() == "b":
        bishops += 1
    if bishops > 1:
        worth += BONUS_PAIR
    return worth


def canonical(move):
    """Order-independent identity used as the final tie-break."""
    return (square(move[:2]), square(move[2:4]), move[4:].lower())


def select(legal, board):
    ordered = sorted(legal, key=canonical)
    return min(ordered, key=lambda mv: (-gain(mv, board), canonical(mv), mv))


def play():
    while True:
        turn = send("/game", {})
        if turn["status"] == "done":
            break
        number = turn["game"]
        while turn["status"] == "your_move":
            board = layout(turn["fen"])
            turn = send("/move", {
                "game": number,
                "move": select(turn["legal_moves"], board),
            })
        print(f"game {number}: {turn['outcome']}", file=sys.stderr)
    print("done", file=sys.stderr)


play()

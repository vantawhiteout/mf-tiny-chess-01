# Tiny one-file chess bot for the make.fun tiny-chess-01 bounty.
# Speaks the minimal JSON protocol over MAKEFUN_ENV_URL; stdlib only.
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env url")

# Material values (pawn = 1) and small placement tables.
PIECE = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}
PAWN_RANK = [0, 0, 1, 2, 4, 8, 16, 0]
KNIGHT_RANK = [-4, -2, 0, 1, 1, 0, -2, -4]
BISHOP_PAIR = 0.5  # small bonus when both bishops are still on the board


def call(path, body):
    request = urllib.request.Request(
        URL + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.HTTPError as err:
        sys.exit(f"{path}: HTTP {err.code}")


def parse_board(fen):
    """Map each occupied square ('a1'..'h8') to its piece letter."""
    squares = {}
    for row_index, row in enumerate(fen.split()[0].split("/")):
        file_index = 0
        for char in row:
            if char.isdigit():
                file_index += int(char)
            else:
                squares["abcdefgh"[file_index] + str(8 - row_index)] = char
                file_index += 1
    return squares


def choose(fen, legal):
    board = parse_board(fen)

    def rank(move):
        origin, target = move[:2], move[2:4]
        mover = board[origin].lower()
        white_side = board[origin].isupper()
        victim = board.get(target)
        en_passant = victim is None and mover == "p" and origin[0] != target[0]
        if en_passant:
            victim = "p"
        gain = PIECE[victim.lower()] if victim else 0
        promotion = PIECE[move[4]] if len(move) == 5 else 0
        placement = 0
        if mover == "p":
            placement = PAWN_RANK[int(target[1]) - 1] - PAWN_RANK[int(origin[1]) - 1]
        elif mover == "n":
            placement = KNIGHT_RANK[int(target[1]) - 1] - KNIGHT_RANK[int(origin[1]) - 1]

        # Count bishops belonging to the mover after this move: the target
        # square is left or captured, while a promotion may add a bishop.
        bishops = sum(
            1 for square, piece in board.items()
            if square != target and piece.lower() == "b" and piece.isupper() == white_side
        )
        if len(move) == 5 and move[4] == "b":
            bishops += 1
        pair = BISHOP_PAIR if bishops >= 2 else 0

        return (-gain - promotion * 2 - placement - pair, -promotion, PIECE[mover], move)

    return min(legal, key=rank)


while True:
    state = call("/game", {})
    if state["status"] == "done":
        break
    while state["status"] == "your_move":
        state = call("/move", {
            "game": state["game"],
            "move": choose(state["fen"], state["legal_moves"]),
        })
    print(f"game {state['game']}: {state['outcome']}", file=sys.stderr)
print("done", file=sys.stderr)

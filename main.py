# Compact chess entry for tiny-chess-01 (MIT). One-file engine, stdlib only.
import json, os, sys, urllib.error, urllib.request

U = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env url")
V = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}
# Tiny piece-square bonuses by rank for pawns and knights.
PR = [0, 0, 1, 2, 4, 8, 16, 0]
NK = [-4, -2, 0, 1, 1, 0, -2, -4]


def post(p, b):
    r = urllib.request.Request(U + p, data=json.dumps(b).encode(), headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            return json.load(x)
    except urllib.error.HTTPError as e:
        sys.exit(f"{p}: HTTP {e.code}")


def bd(f):
    o = {}
    for i, row in enumerate(f.split()[0].split("/")):
        j = 0
        for c in row:
            if c.isdigit():
                j += int(c)
            else:
                o["abcdefgh"[j] + str(8 - i)] = c
                j += 1
    return o


def pick(f, legal):
    b = bd(f)

    def rank(m):
        a, z = m[:2], m[2:4]
        me = b[a].lower()
        them = b.get(z)
        ep = them is None and me == "p" and a[0] != z[0]
        if ep:
            them = "p"
        take = V[them.lower()] if them else 0
        promo = V[m[4]] if len(m) == 5 else 0
        bonus = 0
        if me == "p":
            bonus = PR[int(z[1]) - 1] - PR[int(a[1]) - 1]
        elif me == "n":
            bonus = NK[int(z[1]) - 1] - NK[int(a[1]) - 1]
        return (-take - promo * 2 - bonus, -promo, V[me], m)

    return min(legal, key=rank)


while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": pick(g["fen"], g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']}", file=sys.stderr)
print("done", file=sys.stderr)

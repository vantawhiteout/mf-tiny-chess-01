# Compact 0x88 chess engine for tiny-chess-01.
# Deterministic: fixed node budget, no clocks, no randomness.
import json
import os
import sys
import urllib.error
import urllib.request

ENV = os.environ.get("MAKEFUN_ENV_URL")
if not ENV:
    sys.exit("no env url")

def post(path, body):
    req = urllib.request.Request(ENV + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(path + ": HTTP " + str(e.code))

# ---- board: 0x88, squares a1=0 .. h8=119; +white, -black ----
FENCH = " pnbrqk"
KN = [33,31,18,14,-14,-18,-31,-33]
KG = [1,-1,16,-16,15,17,-15,-17]
BD = [15,17,-15,-17]
RD = [1,-1,16,-16]
MATE = 30000
INF = 32000

def off(s): return bool(s & 0x88)
def name(s): return "abcdefgh"[s & 7] + str((s >> 4) + 1)
def sqof(t): return (int(t[1]) - 1) * 16 + "abcdefgh".index(t[0])

# attack tables for leapers (computed once)
KNATT = []
KGATT = []
PAATT = [[], []]
for s in range(128):
    a = []
    for d in KN:
        t = s + d
        if not off(t): a.append(t)
    KNATT.append(a)
    a = []
    for d in KG:
        t = s + d
        if not off(t): a.append(t)
    KGATT.append(a)
    for c in (0, 1):
        a = []
        for df in (-1, 1):
            t = s + (16 if c == 0 else -16) + df
            if not off(t): a.append(t)
        PAATT[c].append(a)

# zobrist keys from a fixed xorshift generator
_z = 123456789
def _nxt():
    global _z
    _z ^= _z << 13; _z &= 0xffffffff
    _z ^= _z >> 17
    _z ^= _z << 5; _z &= 0xffffffff
    return _z
ZP = [[_nxt() for _ in range(128)] for _ in range(13)]
ZS = _nxt(); ZC = [_nxt() for _ in range(16)]; ZE = [_nxt() for _ in range(8)]

# tapered piece values and simple piece-square formulas
MG = [0,82,337,365,477,1025,0]
EG = [0,94,281,297,512,936,0]
PHASE = [0,0,1,1,2,4,0]
# PeSTO tapered piece-square tables (mg then eg, rank 1 first, a-file first)
TABLES = """
 0 0 0 0 0 0 0 0 98 134 61 95 68 126 34 -11 -6 7 26 31 65 56 25 -20 -14 13 6 21 23 12 17 -23 -27 -2 -5 12 17 6 10 -25 -26 -4 -4 -10 3 3 33 -12 -35 -1 -20 -23 -15 24 38 -22 0 0 0 0 0 0 0 0
-167 -89 -34 -49 61 -97 -15 -107 -73 -41 72 36 23 62 7 -17 -47 60 37 65 84 129 73 44 -9 17 19 53 37 69 18 22 -13 4 16 13 28 19 21 -8 -23 -9 12 10 19 17 25 -16 -29 -53 -12 -3 -1 18 -14 -19 -105 -21 -58 -33 -17 -28 -19 -23
-29 4 -82 -37 -25 -42 7 -8 -26 16 -18 -13 30 59 18 -47 -16 37 43 40 35 50 37 -2 -4 5 19 50 37 37 7 -2 -6 13 13 26 34 12 10 4 0 15 15 15 14 27 18 10 4 15 16 0 7 21 33 1 -33 -3 -14 -21 -13 -12 -39 -21
32 42 32 51 63 9 31 43 27 32 58 62 80 67 26 44 -5 19 26 36 17 45 61 16 -24 -11 7 26 24 35 -8 -20 -36 -26 -12 -1 9 -7 6 -23 -45 -25 -16 -17 3 0 -5 -33 -44 -16 -20 -9 -1 11 -6 -71 -19 -13 1 17 16 7 -37 -26
-28 0 29 12 59 44 43 45 -24 -39 -5 1 -16 57 28 54 -13 -17 7 8 29 56 47 57 -27 -27 -16 -16 -1 17 -2 1 -9 -26 -9 -10 -2 -4 3 -3 -14 2 -11 -2 -5 2 14 5 -35 -8 11 2 8 15 -3 1 -1 -18 -9 10 -15 -25 -31 -50
-65 23 16 -15 -56 -34 2 13 29 -1 -20 -7 -8 -4 -38 -29 -9 24 2 -16 -20 6 22 -22 -17 -20 -12 -27 -30 -25 -14 -36 -49 -1 -27 -39 -46 -44 -33 -51 -14 -14 -22 -46 -44 -30 -15 -27 1 7 -8 -64 -43 -16 9 8 -15 36 12 -54 8 -28 24 14
0 0 0 0 0 0 0 0 178 173 158 134 147 132 165 187 94 100 85 67 56 53 82 84 32 24 13 5 -2 4 17 17 13 9 -3 -7 -7 -8 3 -1 4 7 -6 1 0 -5 -1 -8 13 8 8 10 13 0 2 -7 0 0 0 0 0 0 0 0
-58 -38 -13 -28 -31 -27 -63 -99 -25 -8 -25 -2 -9 -25 -24 -52 -24 -20 10 9 -1 -9 -19 -41 -17 3 22 22 22 11 8 -18 -18 -6 16 25 16 17 4 -18 -23 -3 -1 15 10 -3 -20 -22 -42 -20 -10 -5 -2 -20 -23 -44 -29 -51 -23 -15 -22 -18 -50 -64
-14 -21 -11 -8 -7 -9 -17 -24 -8 -4 7 -12 -3 -13 -4 -14 2 -8 0 -1 -2 6 0 4 -3 9 12 9 14 10 3 2 -6 3 13 19 7 10 -3 -9 -12 -3 8 10 13 3 -7 -15 -14 -18 -7 -1 4 -9 -15 -27 -23 -9 -23 -5 -9 -16 -5 -17
13 10 18 15 12 12 8 5 11 13 13 11 -3 3 8 3 7 7 7 5 4 -3 -5 -3 4 3 13 1 2 1 -1 2 3 5 8 4 -5 -6 -8 -11 -4 0 -5 -1 -7 -12 -8 -16 -6 -6 0 2 -9 -9 -11 -3 -9 2 3 -1 -5 -13 4 -20
-9 22 22 27 27 19 10 20 -17 20 32 41 58 25 30 0 -20 6 9 49 47 35 19 9 3 22 24 45 57 40 57 36 -18 28 19 47 31 34 39 23 -16 -27 15 6 9 17 10 5 -22 -23 -30 -16 -16 -23 -36 -32 -33 -28 -22 -43 -5 -32 -20 -41
-74 -35 -18 -18 -11 15 4 -17 -12 17 14 17 17 38 23 11 10 17 23 15 20 45 44 13 -8 22 24 27 26 33 26 3 -18 -4 21 24 27 23 9 -11 -19 -3 11 21 23 16 7 -9 -27 -11 4 13 14 4 -5 -17 -53 -34 -21 -11 -28 -14 -24 -43
""".split()
T = [list(map(int, TABLES[i*64:(i+1)*64])) for i in range(12)]
PST_MG = [[0]*128 for _ in range(13)]
PST_EG = [[0]*128 for _ in range(13)]
for t in range(1, 7):
    for i in range(64):
        r = i//8; f = i%8
        s = (7-r)*16+f
        m = T[t-1][i]; e = T[t-1+6][i]
        PST_MG[t+6][s] = m; PST_EG[t+6][s] = e
        u = s ^ 112
        PST_MG[-t+6][u] = m; PST_EG[-t+6][u] = e

class Pos:
    def __init__(self, fen):
        self.b = [0]*128
        self.occ = [set(), set()]
        self.king = [-1, -1]
        part = fen.split()
        rows = part[0].split("/")
        for i, row in enumerate(rows):
            f = 0
            for ch in row:
                if ch.isdigit(): f += int(ch)
                else:
                    t = FENCH.index(ch.lower())
                    c = 0 if ch.isupper() else 1
                    s = (7-i)*16+f
                    p = t if c == 0 else -t
                    self.b[s] = p
                    self.occ[c].add(s)
                    if t == 6: self.king[c] = s
                    f += 1
        self.side = 0 if part[1] == "w" else 1
        self.cast = 0
        for ch in part[2]:
            self.cast |= {"K":1,"Q":2,"k":4,"q":8}.get(ch,0)
        self.ep = sqof(part[3]) if len(part) > 3 and part[3] != "-" else -1
        self.half = int(part[4]) if len(part) > 4 else 0
        self.hash = 0
        for s in range(128):
            if self.b[s]: self.hash ^= ZP[self.b[s]+6][s]
        if self.side: self.hash ^= ZS
        self.hash ^= ZC[self.cast]
        if self.ep >= 0: self.hash ^= ZE[self.ep & 7]
        self.hist = []

    def attacked(self, sq, by):
        b = self.b
        # pawns
        for t in PAATT[1-by][sq]:
            if b[t] == (1 if by == 0 else -1): return True
        # knights, king
        for t in KNATT[sq]:
            if b[t] == (2 if by == 0 else -2): return True
        for t in KGATT[sq]:
            if b[t] == (6 if by == 0 else -6): return True
        # sliders
        for dirs, types in ((BD, (3,5)), (RD, (4,5))):
            for d in dirs:
                t = sq + d
                while not off(t):
                    p = b[t]
                    if p:
                        v = abs(p)
                        if (p > 0) == (by == 0) and v in types: return True
                        break
                    t += d
        return False

    def gen(self, caps=False):
        b = self.b
        s = self.side
        sg = 1 if s == 0 else -1
        out = []
        ap = PAATT[s]
        for f in self.occ[s]:
            p = b[f]
            t = abs(p)
            if t == 1:
                one = f + 16*sg
                if not off(one) and b[one] == 0 and not caps:
                    if one >> 4 in (0,7):
                        for pr in (5,4,3,2): out.append(f | one<<7 | pr<<14)
                    else:
                        out.append(f | one<<7)
                        two = one + 16*sg
                        if f >> 4 == (1 if s == 0 else 6) and b[two] == 0:
                            out.append(f | two<<7 | 4<<17)
                for to in ap[f]:
                    v = b[to]
                    if (v*sg < 0 and abs(v) < 6) or to == self.ep:
                        fl = 1<<17 if to == self.ep else 0
                        if to >> 4 in (0,7):
                            for pr in (5,4,3,2): out.append(f | to<<7 | pr<<14 | fl)
                        else: out.append(f | to<<7 | fl)
            elif t == 2:
                for to in KNATT[f]:
                    v = b[to]
                    if v == 0 or (v*sg < 0 and abs(v) < 6): out.append(f | to<<7)
            elif t == 6:
                for to in KGATT[f]:
                    v = b[to]
                    if v == 0 or (v*sg < 0 and abs(v) < 6): out.append(f | to<<7)
            else:
                dirs = BD if t == 3 else RD if t == 4 else BD+RD
                for d in dirs:
                    to = f + d
                    while not off(to):
                        v = b[to]
                        if v == 0:
                            if not caps: out.append(f | to<<7)
                        else:
                            if v*sg < 0 and abs(v) < 6: out.append(f | to<<7)
                            break
                        to += d
        if not caps and self.cast:
            if s == 0:
                if self.cast & 1 and not (b[5] or b[6]) and not self.attacked(4,1) and not self.attacked(5,1) and not self.attacked(6,1):
                    out.append(4 | 6<<7 | 2<<17)
                if self.cast & 2 and not (b[1] or b[2] or b[3]) and not self.attacked(4,1) and not self.attacked(3,1) and not self.attacked(2,1):
                    out.append(4 | 2<<7 | 2<<17)
            else:
                if self.cast & 4 and not (b[117] or b[118]) and not self.attacked(116,0) and not self.attacked(117,0) and not self.attacked(118,0):
                    out.append(116 | 118<<7 | 2<<17)
                if self.cast & 8 and not (b[113] or b[114] or b[115]) and not self.attacked(116,0) and not self.attacked(115,0) and not self.attacked(114,0):
                    out.append(116 | 114<<7 | 2<<17)
        return out

    def make(self, m):
        f = m & 127; to = m>>7 & 127; pr = m>>14 & 7; fl = m>>17
        b = self.b
        p = b[f]; cap = b[to]
        s = self.side
        nc = self.cast & CF[f] & CF[to]
        h = self.hash ^ ZP[p+6][f] ^ ZP[p+6][to] ^ ZS ^ ZC[self.cast] ^ ZC[nc]
        if cap: h ^= ZP[cap+6][to]
        if self.ep >= 0: h ^= ZE[self.ep & 7]
        undo = (p, cap, self.cast, self.ep, self.half, self.hash, f, to)
        occ = self.occ
        occ[s].remove(f); occ[s].add(to)
        b[f] = 0
        b[to] = p
        if pr:
            np = pr if s == 0 else -pr
            b[to] = np
            h ^= ZP[p+6][to] ^ ZP[np+6][to]
        if fl & 1:
            cf = to - 16 if s == 0 else to + 16
            ccap = b[cf]
            b[cf] = 0
            occ[1-s].discard(cf)
            h ^= ZP[ccap+6][cf]
            undo = undo + (cf, ccap)
        else:
            undo = undo + (-1, 0)
        if fl & 2:
            if to == 6: rf, rt = 7, 5
            elif to == 2: rf, rt = 0, 3
            elif to == 118: rf, rt = 119, 117
            else: rf, rt = 112, 115
            rp = b[rf]
            b[rf] = 0; b[rt] = rp
            occ[s].remove(rf); occ[s].add(rt)
            h ^= ZP[rp+6][rf] ^ ZP[rp+6][rt]
            undo = undo + (rf, rp)
        else: undo = undo + (-1, 0)
        if abs(p) == 6: self.king[s] = to
        self.cast = nc
        self.ep = (f+to)//2 if fl & 4 else -1
        if self.ep >= 0: h ^= ZE[self.ep & 7]
        self.half = 0 if abs(p) == 1 or cap or (fl & 1) else self.half+1
        if cap: occ[1-s].discard(to)
        self.hash = h
        self.side = 1-s
        self.hist.append(h)
        return undo

    def unmake(self, m, u):
        f = m & 127; to = m>>7 & 127
        p, cap, cast, ep, half, h, _, _, cf, ccap, rf, rp = u
        b = self.b
        occ = self.occ
        s = 1-self.side
        b[f] = p; b[to] = cap
        occ[s].add(f); occ[s].discard(to)
        if cap: occ[1-s].add(to)
        if cf >= 0:
            b[cf] = ccap; occ[1-s].add(cf)
        if rf >= 0:
            b[rf] = rp
            rt = 5 if to == 6 else 3 if to == 2 else 117 if to == 118 else 115
            b[rt] = 0
            occ[s].add(rf); occ[s].discard(rt)
        if abs(p) == 6: self.king[s] = f
        self.cast = cast; self.ep = ep; self.half = half
        self.hash = h; self.side = s
        self.hist.pop()

    def evaluate(self):
        mg = eg = ph = 0
        b = self.b
        wp = bp = 0
        bs = [0, 0]
        rooks = [[], []]
        for s in self.occ[0]:
            p = b[s]; t = p
            mg += MG[t] + PST_MG[p+6][s]; eg += EG[t] + PST_EG[p+6][s]
            ph += PHASE[t]
            if t == 1: wp |= 1 << SQ64[s]
            elif t == 3: bs[0] += 1
            elif t == 4: rooks[0].append(s&7)
        for s in self.occ[1]:
            p = b[s]; t = -p
            mg -= MG[t] + PST_MG[p+6][s]; eg -= EG[t] + PST_EG[p+6][s]
            ph += PHASE[t]
            if t == 1: bp |= 1 << SQ64[s]
            elif t == 3: bs[1] += 1
            elif t == 4: rooks[1].append(s&7)
        if bs[0] > 1: mg += 35; eg += 20
        if bs[1] > 1: mg -= 35; eg -= 20
        for c, my, opp, sign in ((0,wp,bp,1),(1,bp,wp,-1)):
            pp = my
            while pp:
                bit = pp & -pp; pp ^= bit
                sq = bit.bit_length()-1
                f = sq & 7; fm = FILEMASK[f]; r = sq >> 3
                if (my & fm).bit_count() > 1: mg -= 14*sign; eg -= 20*sign
                if not (my & ADJFILE[f]): mg -= 14*sign; eg -= 16*sign
                if not (opp & PASSED[c][sq]):
                    aa = r if c == 0 else 7-r
                    mg += (8+aa*aa*2)*sign; eg += (12+aa*aa*4)*sign
            for f in rooks[c]:
                fm = FILEMASK[f]
                if not (my & fm):
                    mg += (18 if not (opp & fm) else 9)*sign
                    eg += (12 if not (opp & fm) else 0)*sign
            k = SQ64[self.king[c]]
            kf = k & 7; kr = k >> 3
            shield = (my & SHIELD[c][kr][kf]).bit_count()
            mg -= (4-shield)*10*sign
            if not (my & FILEMASK[kf]): mg -= 12*sign
        if ph > 24: ph = 24
        v = (mg*ph + eg*(24-ph))//24
        return v + (10 if self.side == 0 else -10)

SQ64 = [-1]*128
for _r in range(8):
    for _f in range(8): SQ64[_r*16+_f] = _r*8+_f
FILEMASK = [0x0101010101010101 << _f for _f in range(8)]
ADJFILE = [((FILEMASK[_f-1] if _f else 0) | (FILEMASK[_f+1] if _f < 7 else 0)) for _f in range(8)]
SHIELD = [[[0]*8 for _ in range(8)] for _ in range(2)]
for _c in (0,1):
    for _kf in range(8):
        for _kr in range(8):
            _m = 0
            for _df in (-1,0,1):
                _ff = _kf+_df
                if 0 <= _ff < 8:
                    for _dr in (1,2):
                        _rr = _kr+_dr if _c == 0 else _kr-_dr
                        if 0 <= _rr < 8: _m |= 1 << (_rr*8+_ff)
            SHIELD[_c][_kr][_kf] = _m
PASSED = [[0]*64, [0]*64]
for _sq in range(64):
    _f = _sq & 7; _r = _sq >> 3
    _m = FILEMASK[_f] | ADJFILE[_f]
    PASSED[0][_sq] = _m & ~((1 << ((_r+1)*8)) - 1)
    PASSED[1][_sq] = _m & ((1 << (_r*8)) - 1)

CF = [15]*128
CF[0] = 13; CF[7] = 14; CF[112] = 7; CF[119] = 11
CF[4] = 12; CF[116] = 3

class Search:
    def __init__(self, pos, budget):
        self.p = pos
        self.budget = budget
        self.nodes = 0
        self.tt = {}
        self.kill = [[0,0] for _ in range(80)]
        self.hist = {}
        self.rep = {}

    def qsearch(self, alpha, beta, d):
        self.nodes += 1
        p = self.p
        if p.hist.count(p.hash) >= 2 or p.half >= 100: return 0
        stand = p.evaluate()
        if d < -7: return stand
        inch = p.attacked(p.king[p.side], 1-p.side)
        if not inch:
            if stand >= beta: return stand
            if stand > alpha: alpha = stand
        moves = p.gen(inch == False)
        moves = self.order(moves, 0, inch)
        best = stand if not inch else -INF
        for m in moves:
            u = p.make(m)
            if p.attacked(p.king[1-p.side], p.side):
                p.unmake(m, u); continue
            sc = -self.qsearch(-beta, -alpha, d-1)
            p.unmake(m, u)
            if sc > best: best = sc
            if sc > alpha: alpha = sc
            if alpha >= beta: break
        return best

    def order(self, moves, ttmove, inch):
        p = self.p
        b = p.b
        k = self.kill
        h = self.hist
        def key(m):
            if m == ttmove: return -1000000
            to = m>>7 & 127
            v = b[to]
            pr = m>>14 & 7
            if v or pr or (m>>17 & 1):
                vv = abs(v) if v else 1
                return -10000 - vv*16 + (abs(b[m&127]) if b[m&127] else 1)
            if m in k[min(79,len(p.hist))]: return -5000
            return -h.get((b[m&127], to), 0)
        moves.sort(key=key)
        return moves

    def search(self, alpha, beta, depth, ply, can_null):
        self.nodes += 1
        p = self.p
        if self.nodes > self.budget: return 0
        if p.hist.count(p.hash) >= 2 or p.half >= 100: return 0
        inch = p.attacked(p.king[p.side], 1-p.side)
        if depth <= 0: return self.qsearch(alpha, beta, ply)
        h = p.hash
        ent = self.tt.get(h)
        ttmove = 0
        if ent and ent[0] >= depth and ply:
            d, sc, fl, mv = ent
            ttmove = mv
            if fl == 0: return sc
            if fl == 1 and sc >= beta: return sc
            if fl == 2 and sc <= alpha: return sc
        if ent: ttmove = ent[3]
        if can_null and not inch and depth >= 3 and ply and self.phase() > 3:
            ep0 = p.ep
            nh = h ^ ZS ^ (ZE[ep0 & 7] if ep0 >= 0 else 0)
            p.ep = -1
            p.hist.append(nh)
            p.side ^= 1
            sc = -self.search(-beta, -beta+1, depth-3, ply+1, False)
            p.side ^= 1
            p.hist.pop()
            p.ep = ep0
            if sc >= beta: return beta
        moves = self.order(p.gen(), ttmove, inch)
        best = -INF; bestm = 0
        a0 = alpha
        for i, m in enumerate(moves):
            quiet = not (p.b[m>>7 & 127] or (m>>14 & 7) or (m>>17 & 1))
            u = p.make(m)
            if p.attacked(p.king[1-p.side], p.side):
                p.unmake(m, u); continue
            ext = 0
            red = 0
            if depth >= 3 and quiet and not inch and i >= 4:
                red = 1 if i < 10 else 2
            nd = depth-1-red+ext
            if i == 0:
                sc = -self.search(-beta, -alpha, nd, ply+1, True)
            else:
                sc = -self.search(-alpha-1, -alpha, nd, ply+1, True)
                if sc > alpha and red:
                    sc = -self.search(-alpha-1, -alpha, depth-1+ext, ply+1, True)
                if alpha < sc < beta:
                    sc = -self.search(-beta, -alpha, depth-1+ext, ply+1, True)
            p.unmake(m, u)
            if self.nodes > self.budget: return 0
            if sc > best:
                best = sc; bestm = m
            if sc > alpha:
                alpha = sc
                if quiet:
                    kk = self.kill[min(79,ply)]
                    if m != kk[0]: kk[1] = kk[0]; kk[0] = m
                    key0 = (p.b[m&127], m>>7 & 127)
                    self.hist[key0] = self.hist.get(key0,0) + depth*depth
            if alpha >= beta: break
        fl = 0 if a0 < best < beta else 1 if best >= beta else 2
        if len(self.tt) > 120000: self.tt.clear()
        self.tt[h] = (depth, best, fl, bestm)
        return best

    def phase(self):
        ph = 0
        for c in (0,1):
            for s in self.p.occ[c]: ph += PHASE[abs(self.p.b[s])]
        return ph

    def best(self, legal):
        p = self.p
        p.hist.append(p.hash)
        legal = [sqof(m[:2]) | sqof(m[2:4])<<7 | ("nbrq".index(m[4])+2 if len(m)>4 else 0)<<14 for m in legal]
        root = self.order(legal, 0, False)
        bestm = root[0]
        bm = None
        for d in range(1, 40):
            alpha = -INF; beta = INF
            scores = []
            for i, m in enumerate(root):
                u = p.make(m)
                if p.attacked(p.king[1-p.side], p.side):
                    p.unmake(m, u); continue
                if i == 0:
                    sc = -self.search(-beta, -alpha, d-1, 1, True)
                else:
                    sc = -self.search(-alpha-1, -alpha, d-1, 1, True)
                    if alpha < sc < beta:
                        sc = -self.search(-beta, -alpha, d-1, 1, True)
                p.unmake(m, u)
                if self.nodes > self.budget: break
                scores.append((sc, m))
                if sc > alpha: alpha = sc; bestm = m
            if self.nodes > self.budget or not scores: break
            bm = bestm
            root.sort(key=lambda m: -next((s for s,x in scores if x == m), -INF))
        f = (bm or bestm) & 127; t = (bm or bestm)>>7 & 127; pr = (bm or bestm)>>14 & 7
        return name(f)+name(t)+("nbrq"[pr-2] if pr else "")

BUDGET = 60000
while True:
    g = post("/game", {})
    if g["status"] == "done": break
    while g["status"] == "your_move":
        p = Pos(g["fen"])
        s = Search(p, BUDGET)
        mv = s.best(g["legal_moves"])
        g = post("/move", {"game": g["game"], "move": mv})
    print("game", g["game"], g["outcome"], g["reason"], file=sys.stderr)
print("done", g.get("wins"), g.get("draws"), g.get("losses"), file=sys.stderr)

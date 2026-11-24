"""Reproducible numerical checks for "The Prime Helix" (version 2).

Run:  python3 analysis/prime_helix_checks.py
Writes analysis/results.txt and the figures in figures/.
Needs numpy and matplotlib. The largest sieve (primes up to 10^8) uses about
100 MB of memory and takes a minute or two.

Sections
  1. Decay of delta(N) = R(N) - 1/sqrt(2) for the chord-hopper ratio
  2. Chord shapes on the linear helix (screw symmetry): one shape per gap
  3. Turn angles and repeated gaps: real primes vs Cramer and Granville models
  4. The logarithmic-winding walk: resonance peaks at the zeta zeros
"""
import os
from collections import Counter

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
OUT = []

# First zeros of zeta (imaginary parts), from Odlyzko's tables
ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
         37.586178, 40.918719, 43.327073, 48.005151, 49.773832]


def log(line=""):
    print(line)
    OUT.append(line)


def sieve(n):
    s = np.ones(n + 1, bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return s


def prime_powers(n, s):
    """Prime powers up to n with von Mangoldt weights, sorted by n."""
    ns, lam = [], []
    for p in np.nonzero(s)[0]:
        q = int(p)
        lp = np.log(p)
        while q <= n:
            ns.append(q)
            lam.append(lp)
            q *= int(p)
    o = np.argsort(ns)
    return np.array(ns, float)[o], np.array(lam)[o]


plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.spines.top": False,
                     "axes.spines.right": False})

# ---------------------------------------------------------------- 1. delta(N)
log("1. Decay of delta(N) = R(N) - 1/sqrt(2)")
X1 = 10 ** 8
s1 = sieve(X1)
p1 = np.nonzero(s1)[0].astype(float)
g1 = np.diff(p1)
D = np.cumsum(np.sqrt(2 - 2 * np.cos(g1) + g1 * g1))
log(f"{'N':>9} {'p_N':>11} {'R(N)':>9} {'delta':>9} {'delta*ln^2 p':>13} {'(ln p)^2/sqrt p':>16}")
rows = []
for N in [8000, 10 ** 4, 10 ** 5, 10 ** 6, 5 * 10 ** 6]:
    pN = p1[N - 1]
    R = D[N - 2] / ((pN - 2) * np.sqrt(2))
    dl = R - 1 / np.sqrt(2)
    rows.append((N, pN, R, dl))
    log(f"{N:>9} {pN:>11.0f} {R:>9.6f} {dl:>9.5f} {dl * np.log(pN) ** 2:>13.3f} "
        f"{np.log(pN) ** 2 / np.sqrt(pN):>16.5f}")
idx = np.unique(np.logspace(2, np.log10(len(g1) - 1), 300).astype(int))
pN = p1[idx]
Rn = D[idx - 1] / ((pN - 2) * np.sqrt(2))
dl = Rn - 1 / np.sqrt(2)
fig, ax = plt.subplots(1, 2, figsize=(8, 3.1))
ax[0].loglog(pN, dl, color="#0f6e8c", lw=1.6, label=r"measured $\delta(N)$")
ax[0].loglog(pN, 1.6 / np.log(pN) ** 2, "--", color="#555", lw=1, label=r"$1.6/\ln^2 p_N$")
ax[0].loglog(pN, np.log(pN) ** 2 / np.sqrt(pN), ":", color="#b8541a", lw=1.2,
             label=r"$(\ln p_N)^2/\sqrt{p_N}$ (v1 heuristic)")
ax[0].set_xlabel(r"$p_N$")
ax[0].set_ylabel(r"$\delta(N)$")
ax[0].legend(fontsize=7, frameon=False)
ax[1].semilogx(pN, dl * np.log(pN) ** 2, color="#0f6e8c", lw=1.6)
ax[1].set_xlabel(r"$p_N$")
ax[1].set_ylabel(r"$\delta(N)\,\ln^2 p_N$")
ax[1].set_ylim(0, 2.2)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_delta_decay.png"))
plt.close(fig)
del s1, D

# ---------------------------------------------------------- 2. chord shapes
log()
log("2. Chord shapes on the helix (cos t, sin t, t), primes > 3 up to 10^7")
X2 = 10 ** 7
s2 = sieve(X2)
p2 = np.nonzero(s2)[0]
p2 = p2[p2 > 3]
g2 = np.diff(p2)
L = np.sqrt(2 - 2 * np.cos(g2) + g2 ** 2.0)
tilt = np.arctan2(g2, 2 * np.abs(np.sin(g2 / 2)))
shapes = set(zip(np.round(L, 9), np.round(tilt, 9)))
log(f"chords: {len(g2)}, distinct gaps: {len(set(g2))}, distinct (length, tilt) shapes: {len(shapes)}")
az = np.mod(p2, 2 * np.pi)
h, _ = np.histogram(az, bins=12, range=(0, 2 * np.pi))
log("azimuth p mod 2pi, 12 bins relative to mean: " + " ".join(f"{v:.3f}" for v in h / h.mean()))

# ---------------------------------------------- 3. turn angles and repeats
log()
log("3. Turn angles and repeated gaps (n in (1000, 10^7])")
start = 1000
n = np.arange(X2 + 1)
real = np.nonzero(s2)[0]
real = real[real > start]
rng = np.random.default_rng(1)
m = n[start + 1:].astype(float)
cram = n[start + 1:][rng.random(len(m)) < 1 / np.log(m)]


def granville(wheel_primes, seed):
    W = int(np.prod(wheel_primes))
    phi = int(np.prod([q - 1 for q in wheel_primes]))
    cop = np.ones(X2 + 1, bool)
    for q in wheel_primes:
        cop &= (n % q != 0)
    cop[:start + 1] = False
    ii = np.nonzero(cop)[0]
    r = np.random.default_rng(seed)
    return ii[r.random(len(ii)) < (W / phi) / np.log(ii.astype(float))]


# helix radius r, winding w per unit, rise c per unit; turn angle depends only on (g1, g2)
r_, w_, c_ = 1.0, 1.0, 1.0  # the helix (cos t, sin t, t) used throughout the paper


def turn(g):
    a, b = g[:-1].astype(float), g[1:].astype(float)
    ha, hb = 2 * r_ * np.sin(w_ * a / 2), 2 * r_ * np.sin(w_ * b / 2)
    dot = ha * hb * np.cos(w_ * (a + b) / 2) + c_ * c_ * a * b
    la, lb = np.sqrt(ha ** 2 + (c_ * a) ** 2), np.sqrt(hb ** 2 + (c_ * b) ** 2)
    return np.degrees(np.arccos(np.clip(dot / (la * lb), -1, 1)))


GAPS = [6, 12, 18, 24, 30]


def repeat_ratios(P):
    g = np.diff(P)
    cnt = Counter(g.tolist())
    tot = len(g)
    pairs = Counter(zip(g[:-1].tolist(), g[1:].tolist()))
    return [(pairs[(k, k)] / (tot - 1)) / ((cnt[k] / tot) ** 2) for k in GAPS]


bins = np.arange(0, 90, 15)
hist = {}
gran7 = granville((2, 3, 5, 7), 1)
for name, P in [("real", real), ("cramer", cram), ("granville_2357", gran7)]:
    t = turn(np.diff(P))
    hh, _ = np.histogram(t, bins=bins)
    hist[name] = 100 * hh / hh.sum()
    log(f"{name:>15}: turn-angle % per 15 deg bin: " + " ".join(f"{v:5.2f}" for v in hist[name]))
rr_real = repeat_ratios(real)
rr_cram = repeat_ratios(cram)
G13 = np.array([repeat_ratios(granville((2, 3, 5, 7, 11, 13), sd)) for sd in range(8)])
G7 = np.array([repeat_ratios(granville((2, 3, 5, 7), sd)) for sd in range(8)])
log("repeat ratio P(g,g)/P(g)^2 for g = " + ", ".join(map(str, GAPS)))
log("  real primes        : " + " ".join(f"{v:.3f}" for v in rr_real))
log("  Cramer (1 run)     : " + " ".join(f"{v:.3f}" for v in rr_cram))
log("  Granville to 7     : " + " ".join(f"{a:.3f}+-{b:.3f}" for a, b in zip(G7.mean(0), G7.std(0))))
log("  Granville to 13    : " + " ".join(f"{a:.3f}+-{b:.3f}" for a, b in zip(G13.mean(0), G13.std(0))))

fig, ax = plt.subplots(1, 2, figsize=(8, 3.1))
xc = bins[:-1] + 7.5
wbar = 4.2
ax[0].bar(xc - wbar, hist["real"], wbar, label="real primes", color="#0f6e8c")
ax[0].bar(xc, hist["granville_2357"], wbar, label="Granville model", color="#7fb6c8")
ax[0].bar(xc + wbar, hist["cramer"], wbar, label="Cramér model", color="#c9a27e")
ax[0].set_xlabel("turn angle between consecutive chords (deg)")
ax[0].set_ylabel("% of chord pairs")
ax[0].legend(fontsize=7, frameon=False)
xg = np.arange(len(GAPS))
ax[1].bar(xg - 0.27, rr_real, 0.27, color="#0f6e8c", label="real primes")
ax[1].bar(xg, G13.mean(0), 0.27, yerr=G13.std(0), color="#7fb6c8", capsize=2,
          label="Granville, sieved to 13")
ax[1].bar(xg + 0.27, rr_cram, 0.27, color="#c9a27e", label="Cramér")
ax[1].axhline(1, color="#555", lw=0.8)
ax[1].set_xticks(xg, [f"{k}" for k in GAPS])
ax[1].set_xlabel("repeated gap g")
ax[1].set_ylabel(r"$P(g,g)\,/\,P(g)^2$")
ax[1].set_ylim(0, 1.25)
ax[1].legend(fontsize=7, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_turn_repeats.png"))
plt.close(fig)
del s2, n

# --------------------------------------------------- 4. log-winding walk
log()
log("4. Logarithmic-winding walk H(t) = sum Lambda(n) n^(-1/2 - i t), pole term removed")
X4 = 2 * 10 ** 6
s4 = sieve(X4)
nn, lam = prime_powers(X4, s4)
lnn = np.log(nn)
taper = (1 - nn / X4) ** 2
wts = taper * lam / np.sqrt(nn)


def pole_term(t, X):
    # integral_1^X (1 - x/X)^2 x^(-s) dx with s = 1/2 + i t, in closed form
    sc = complex(0.5, t)
    tot = 0
    for k, ck in enumerate([1.0, -2.0 / X, 1.0 / X ** 2]):
        a = k + 1 - sc
        tot += ck * (np.exp(a * np.log(X)) - 1) / a
    return tot


th = np.arange(8, 50, 0.01)
A = np.array([abs(np.sum(wts * np.exp(-1j * t * lnn)) - pole_term(t, X4)) for t in th])
pk = [i for i in range(1, len(th) - 1) if A[i] > A[i - 1] and A[i] > A[i + 1] and A[i] > 0.3 * A.max()]
log("peak t  vs  known zero gamma")
for i in pk:
    z = min(ZEROS, key=lambda zz: abs(zz - th[i]))
    log(f"  {th[i]:7.2f}   {z:10.6f}")

fig, ax = plt.subplots(figsize=(8, 2.6))
for z in ZEROS:
    ax.axvline(z, color="#999", ls="--", lw=0.7)
ax.plot(th, A, color="#0f6e8c", lw=1.2)
ax.set_xlabel(r"winding rate $t$")
ax.set_ylabel(r"$|H_X(t)|$")
ax.set_xlim(8, 50)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_log_spectrum.png"))
plt.close(fig)

# the walk itself at a zero and between zeros, N = 10^5 (no taper)
N5 = 10 ** 5
k5 = nn <= N5
n5, l5 = nn[k5], lam[k5]
log()
log("Walk W_t(N) for N = 10^5 (end point; -ln N = %.2f)" % -np.log(N5))
fig, ax = plt.subplots(1, 2, figsize=(8, 3.6))
for j, t in enumerate([ZEROS[0], 15.0]):
    ph = np.exp(-1j * t * np.log(n5))
    S = np.cumsum(l5 / np.sqrt(n5) * ph)
    C = (np.sqrt(n5) * ph - 1) / complex(0.5, -t)
    Wt = np.concatenate([[0], S - C])
    log(f"  t = {t:9.6f}: W(N) = {Wt[-1].real:.2f} {Wt[-1].imag:+.2f}i, max |W| = {np.abs(Wt).max():.2f}")
    segs = np.stack([np.column_stack([Wt[:-1].real, Wt[:-1].imag]),
                     np.column_stack([Wt[1:].real, Wt[1:].imag])], axis=1)
    lc = LineCollection(segs, colors=plt.cm.viridis(np.linspace(0.15, 0.95, len(segs))), lw=0.6)
    ax[j].add_collection(lc)
    ax[j].autoscale()
    ax[j].plot(0, 0, "o", mfc="none", mec="k")
    ax[j].plot(Wt[-1].real, Wt[-1].imag, "o", color="#b8541a")
    ax[j].set_aspect("equal", adjustable="datalim")
    ax[j].set_title(r"$t = %.4f$" % t + (r" $(=\gamma_1)$" if j == 0 else " (between zeros)"), fontsize=9)
    ax[j].set_xlabel("Re")
    ax[j].set_ylabel("Im")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_log_walk.png"))
plt.close(fig)

with open(os.path.join(HERE, "results.txt"), "w") as f:
    f.write("\n".join(OUT) + "\n")
print("\nwrote analysis/results.txt and figures/*.png")

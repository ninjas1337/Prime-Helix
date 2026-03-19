# Prime Helix

**A geometric exploration of prime distribution on Euler's helix — two particles, one ratio, and a different way to look at the Riemann zeta function.**

---

## What is this?

Euler's identity $e^{i\theta} = \cos\theta + i\sin\theta$ is usually shown as a circle. But if you let $\theta$ run freely in three dimensions, it becomes a helix: $(\cos t, \sin t, t)$.

This project places the prime numbers on that helix, connects consecutive primes with straight-line chords, and asks a simple question: if two particles travel at the same speed — one along the helix, the other hopping chord to chord between primes — what is the ratio of their paths?

The answer converges to $1/\sqrt{2} = \cos(45°)$, determined by the helix geometry alone. The fluctuations around that limit carry information about prime gaps, and appear to reflect the same phenomena captured by the Riemann zeta function — expressed in purely geometric and kinematic terms.

## Interactive Visualizations

All visualizations are standalone HTML files. No build step, no dependencies — just open them in a browser.

| File | Description |
|------|-------------|
| `prime_helix.html` | 3D visualization of primes on the helix with connecting chords. Drag to orbit, scroll to zoom, hover for values. Uses Three.js. |
| `prime_helix_ratio.html` | The two-particle experiment. Shows the convergence of R(N) → 1/√2, local chord/arc ratios per gap, and summary metrics. |
| `prime_phase_function.html` | Dual panel: phasor circle projection (showing caustic rings) and the phase function θ(n) = pₙ mod 2π (showing diagonal striations). |
| `prime_arc_vector.html` | The arc vector function F(n) = path/displacement, its convergence to 1, and π(x) vs Li(x) comparison. |


## The Paper

The `paper/` directory contains the LaTeX source and figures for the working paper:

> **The Prime Helix: A Geometric and Kinematic Translation of Prime Distribution Theory**

The paper presents the construction, derives the chord length formula, defines the two-particle experiment, and draws tentative connections to the prime number theorem, Euler's product formula, the pole at s = 1, and the oscillatory corrections from zeta zeros. It is exploratory in nature — it does not prove new theorems, but proposes a complementary geometric perspective that may offer fresh intuition.


## Key Results

- **R(N) → 1/√2 ≈ 0.70711**: The chord hopper's path converges to cos(45°) of the helix walker's path, a consequence of the prime number theorem and the helix's pitch angle.
- **Caustic rings**: Projecting the chord structure onto the unit circle produces concentric rings whose radii correspond to prime gap sizes and whose brightness reflects gap frequencies.
- **Phase function striations**: Plotting θ(n) = pₙ mod 2π against n reveals diagonal bands — a geometric spectrogram of the primes produced without Fourier analysis.
- **F(n) → 1**: The arc vector function (total chord path / displacement) converges to unity, meaning the prime chord path is asymptotically straight.

## Limitations

This is an exploratory work. The convergence of R(N) follows from elementary analysis once the prime number theorem is assumed. The analogies to the Euler product, the pole at s = 1, and the critical line are suggestive but not rigorous. The visualizations display known properties of prime gaps in a new geometric format rather than revealing previously unknown structure.

## Structure

```
prime-helix/
├── README.md
├── prime_helix.html              # 3D helix visualization
├── prime_helix_ratio.html        # Two-particle convergence
├── prime_phase_function.html     # Phasor circle + phase function
├── prime_arc_vector.html         # Arc vector function F(n)
└── paper/
    ├── prime_helix_paper.tex     # LaTeX source
    ├── prime_helix.png           # Figure 1: 3D helix
    ├── fig_convergence.png       # Figure 2: R(N) convergence
    ├── fig_phasor.png            # Figure 3: Caustic rings
    └── fig_theta.png             # Figure 4: Phase function
```

## License

This work is shared for academic and educational purposes. If you use it, a citation would be appreciated.

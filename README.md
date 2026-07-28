# Calculus, explained

A long-form ManimGL animation that builds calculus from the ground up, in the
spirit of 3Blue1Brown's *Essence of Calculus*.

The running example is `f(x) = x²`, chosen so the Fundamental Theorem closes
the loop neatly: `d/dx x² = 2x`, `∫ x² dx = x³/3`, and `d/dx (x³/3) = x²`.

## What it covers

1. **The hook** — a moving object's position `s(t)=t²`, and the question
   "how fast is it going *right now*?"
2. **Limits** — secant lines collapsing to a tangent as `h → 0`
3. **The derivative** — the difference quotient, slope-of-tangent, and the
   derivative *as a function* (a point slides on `f` while `f'` is traced on a
   second graph)
4. **The power rule** — derived term-by-term from the difference quotient,
   then `d/dx xⁿ = n·xⁿ⁻¹`
5. **Integrals** — area under a curve via Riemann sums (`n = 4 → 8 → 16 → 32 → 64`)
6. **The Fundamental Theorem** — `F(x)=∫ₐˣf`, `dF/dx = f`, and
   `∫ₐᵇf = F(b)−F(a)`: derivatives and integrals are inverses
7. **Why it matters** — position → velocity → acceleration, area = distance,
   optimization; outro

## Render locally

```bash
pip install -r requirements.txt
manimgl scene.py Calculus -w          # default quality
manimgl scene.py Calculus -w --uhd    # 4K
```

## Render on GitHub Actions

`.github/workflows/render.yml` renders the video headlessly (ManimGL under
`xvfb` with software Mesa / `llvmpipe`, plus `texlive` for the LaTeX math) and
attaches the `.mp4` to a `latest` release:

https://github.com/krishn03id/calculus-explained/releases/latest

Built with [ManimGL](https://github.com/3b1b/manim), 3Blue1Brown's animation
engine.

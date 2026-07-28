from manimlib import *
import numpy as np

# The running example throughout the video:  f(x) = x^2
#   derivative      f'(x) = 2x
#   antiderivative  F(x)  = x^3 / 3
# so the Fundamental Theorem closes the loop:  d/dx (x^3/3) = x^2.
def f(x):  return x ** 2
def fp(x): return 2.0 * x
def F(x):  return x ** 3 / 3.0

X0 = 1.0               # point where we study the limit / tangent
A_INT, B_INT = 0.0, 3.0   # integration bounds


class Calculus(Scene):
    def construct(self):
        self.beat_intro()
        self.beat_limit()
        self.beat_derivative()
        self.beat_power_rule()
        self.beat_integral()
        self.beat_ftc()
        self.beat_outro()

    # ---------- helpers ----------
    def tangent_line(self, axes, x0, half=1.0, color=YELLOW):
        y0, m = f(x0), fp(x0)
        x1, x2 = x0 - half, x0 + half
        return Line(
            axes.c2p(x1, y0 + m * (x1 - x0)),
            axes.c2p(x2, y0 + m * (x2 - x0)),
            color=color, stroke_width=3,
        )

    def tan_ends(self, axes, x0, half):
        y0, m = f(x0), fp(x0)
        x1, x2 = x0 - half, x0 + half
        return (
            axes.c2p(x1, y0 + m * (x1 - x0)),
            axes.c2p(x2, y0 + m * (x2 - x0)),
        )

    def riemann(self, axes, n, a, b):
        dx = (b - a) / n
        xu = axes.x_axis.get_unit_size()
        yu = axes.y_axis.get_unit_size()
        rects = VGroup()
        total = 0.0
        for i in range(n):
            x = a + i * dx
            hgt = f(x + dx)               # right-endpoint height
            total += hgt * dx
            rect = Rectangle(
                width=dx * xu, height=hgt * yu,
                fill_color=BLUE_E, fill_opacity=0.6,
                stroke_color=WHITE, stroke_width=max(0.5, 3.0 / n),
            )
            rect.move_to(axes.c2p(x + dx / 2, hgt / 2))
            rects.add(rect)
        return rects, total

    # ---------- 1. the hook: instantaneous speed ----------
    def beat_intro(self):
        title = Text("Calculus", font_size=84, color=WHITE)
        sub = Text("the mathematics of continuous change", font_size=34, color=GREY_B)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.4)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, sub)))

        axes = Axes(x_range=(0, 4.5, 1), y_range=(0, 20, 5), width=9, height=4.5)
        axes.to_edge(DOWN, buff=1.0)
        t_lab = Tex("t", font_size=30).next_to(axes.x_axis, RIGHT)
        s_lab = Tex("s(t)", font_size=30).next_to(axes.y_axis, UP)
        graph = axes.get_graph(lambda t: t ** 2, x_range=[0, 4.3], color=BLUE, stroke_width=3)
        cap = Text("position   s(t) = t²", font_size=28, color=BLUE)
        cap.to_edge(UP, buff=0.5)

        self.play(ShowCreation(axes), Write(t_lab), Write(s_lab))
        self.play(ShowCreation(graph), Write(cap))

        t_tr = ValueTracker(0.0)
        get_t = t_tr.get_value
        dot = Dot(axes.c2p(0, 0), color=RED)
        dot.add_updater(lambda m: m.move_to(axes.c2p(get_t(), get_t() ** 2)))
        self.add(dot)
        self.play(t_tr.animate.set_value(4.2), run_time=4, rate_func=linear)
        self.wait(0.3)

        q = Text("How fast is it moving right now?", font_size=30, color=YELLOW)
        q.to_edge(UP, buff=0.5)
        self.play(Transform(cap, q))
        ans = Text("That question is what calculus was invented to answer.",
                   font_size=26, color=GREY_B)
        ans.next_to(q, DOWN, buff=0.4)
        self.play(Write(ans))
        self.wait(1.5)
        self.play(FadeOut(axes), FadeOut(t_lab), FadeOut(s_lab), FadeOut(graph),
                  FadeOut(cap), FadeOut(ans), FadeOut(dot))

    # ---------- 2. limits: secants collapse to a tangent ----------
    def beat_limit(self):
        axes = Axes(x_range=(-0.5, 2.8, 0.5), y_range=(-0.5, 4.5, 1), width=8, height=5)
        axes.center()
        graph = axes.get_graph(f, x_range=[-0.3, 2.6], color=BLUE, stroke_width=3)
        P = Dot(axes.c2p(X0, f(X0)), color=RED)
        P_label = Tex("(1, 1)", font_size=28, color=RED)
        P_label.next_to(P, LEFT, buff=0.2)
        cap = Text("What is the slope at a single point?", font_size=26)
        cap.to_edge(UP, buff=0.4)

        self.play(ShowCreation(axes), ShowCreation(graph))
        self.play(FadeIn(P), Write(P_label), Write(cap))
        self.wait(0.6)

        hs = [1.5, 1.0, 0.5, 0.2, 0.05]
        slope_tex = Tex("slope = 3.50", font_size=32, color=YELLOW)
        slope_tex.to_corner(UR)
        self.play(FadeIn(slope_tex))
        for h in hs:
            sec = Line(axes.c2p(X0, f(X0)), axes.c2p(X0 + h, f(X0 + h)),
                       color=YELLOW, stroke_width=3)
            slope = (f(X0 + h) - f(X0)) / h
            new = Tex(f"slope = {slope:.2f}", font_size=32, color=YELLOW)
            new.to_corner(UR)
            self.play(ShowCreation(sec), Transform(slope_tex, new), run_time=0.6)
            self.wait(0.2)
            self.play(FadeOut(sec), run_time=0.25)

        tan = self.tangent_line(axes, X0, half=1.2, color=YELLOW)
        final_slope = Tex("slope = 2.00", font_size=32, color=YELLOW)
        final_slope.to_corner(UR)
        self.play(ShowCreation(tan), Transform(slope_tex, final_slope))
        note = Text("as h → 0, the secant becomes the tangent", font_size=24, color=GREY_B)
        note.to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(0.8)
        lim = Tex(r"\lim_{h \to 0} \frac{f(1+h)-f(1)}{h} = 2", font_size=34)
        lim.to_edge(DOWN, buff=1.2)
        self.play(Write(lim))
        self.wait(1.5)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(P), FadeOut(P_label),
                  FadeOut(cap), FadeOut(slope_tex), FadeOut(tan), FadeOut(note), FadeOut(lim))

    # ---------- 3. the derivative (definition + dual-graph trace) ----------
    def beat_derivative(self):
        defn = Tex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}", font_size=40)
        defn.to_edge(UP, buff=0.4)
        self.play(Write(defn))
        geom = Text("= slope of the tangent line at x", font_size=24, color=GREY_B)
        geom.next_to(defn, DOWN, buff=0.3)
        self.play(Write(geom))
        self.wait(1.2)
        self.play(FadeOut(defn), FadeOut(geom))

        axes_f = Axes(x_range=(-2.5, 2.5, 1), y_range=(0, 6, 2), width=10, height=3.2)
        axes_f.to_edge(UP, buff=1.1)
        axes_fp = Axes(x_range=(-2.5, 2.5, 1), y_range=(-5, 5, 2), width=10, height=3.0)
        axes_fp.to_edge(DOWN, buff=1.1)
        g_f = axes_f.get_graph(f, x_range=[-2.3, 2.3], color=BLUE, stroke_width=3)
        lab_f = Tex("f(x) = x^2", font_size=26, color=BLUE)
        lab_f.next_to(axes_f, RIGHT, buff=0.2)
        lab_fp = Tex("f'(x) = ?", font_size=26, color=YELLOW)
        lab_fp.next_to(axes_fp, RIGHT, buff=0.2)

        self.play(ShowCreation(axes_f), ShowCreation(g_f), Write(lab_f))
        self.play(ShowCreation(axes_fp), Write(lab_fp))

        x_tr = ValueTracker(-2.3)
        get_x = x_tr.get_value
        dot_f = Dot(axes_f.c2p(-2.3, f(-2.3)), color=RED)
        dot_f.add_updater(lambda m: m.move_to(axes_f.c2p(get_x(), f(get_x()))))
        tan = self.tangent_line(axes_f, -2.3, half=1.0, color=YELLOW)
        tan.add_updater(lambda m: m.put_start_and_end_on(*self.tan_ends(axes_f, get_x(), 1.0)))
        self.add(dot_f, tan)
        self.play(x_tr.animate.set_value(2.3), run_time=4)
        self.wait(0.4)

        # reset, then trace f' on the lower axes
        self.play(x_tr.animate.set_value(-2.3), run_time=1.2)
        dot_fp = Dot(axes_fp.c2p(-2.3, fp(-2.3)), color=YELLOW)
        dot_fp.add_updater(lambda m: m.move_to(axes_fp.c2p(get_x(), fp(get_x()))))
        trace = TracedPath(dot_fp.get_center, stroke_color=YELLOW, stroke_width=3)
        new_lab = Tex("f'(x) = 2x", font_size=26, color=YELLOW)
        new_lab.next_to(axes_fp, RIGHT, buff=0.2)
        self.add(dot_fp, trace)
        self.play(x_tr.animate.set_value(2.3), run_time=5)
        self.play(Transform(lab_fp, new_lab))
        self.wait(0.8)

        note = Tex(r"\frac{dy}{dx} = f'(x) = 2x", font_size=32)
        note.to_edge(UP, buff=0.4)
        self.play(Write(note))
        self.wait(1.5)
        # Freeze updaters before fading: TracedPath keeps appending points each
        # frame, which mismatches point counts mid-FadeOut and raises broadcast errors.
        for mob in (dot_f, tan, dot_fp, trace):
            mob.clear_updaters()
        self.play(FadeOut(axes_f), FadeOut(axes_fp), FadeOut(g_f), FadeOut(lab_f),
                  FadeOut(lab_fp), FadeOut(dot_f), FadeOut(tan), FadeOut(dot_fp),
                  FadeOut(trace), FadeOut(note))

    # ---------- 4. the power rule, derived ----------
    def beat_power_rule(self):
        title = Text("Why is the derivative of x² equal to 2x?", font_size=30)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        steps = [
            r"\frac{d}{dx}x^2 = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h}",
            r"= \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h}",
            r"= \lim_{h \to 0} \frac{2xh + h^2}{h}",
            r"= \lim_{h \to 0} (2x + h)",
            r"= 2x",
        ]
        lines = VGroup(*[Tex(s, font_size=34) for s in steps])
        lines.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lines.next_to(title, DOWN, buff=0.6)
        for ln in lines:
            self.play(Write(ln), run_time=0.8)
            self.wait(0.35)
        self.wait(0.8)
        self.play(FadeOut(lines))

        rule = Tex(r"\frac{d}{dx} x^n = n\, x^{n-1}", font_size=44, color=YELLOW)
        rule.to_edge(DOWN, buff=1.6)
        box = SurroundingRectangle(rule, color=GOLD, buff=0.2)
        self.play(Write(rule), ShowCreation(box))
        pat = Tex(r"x^1 \to 1 \quad x^2 \to 2x \quad x^3 \to 3x^2", font_size=30)
        pat.next_to(rule, DOWN, buff=0.5)
        self.play(Write(pat))
        self.wait(1.8)
        self.play(FadeOut(title), FadeOut(rule), FadeOut(box), FadeOut(pat))

    # ---------- 5. integrals: area under a curve via Riemann sums ----------
    def beat_integral(self):
        pivot = Text("Derivatives break change down.   Integrals build it up.",
                     font_size=28)
        pivot.to_edge(UP, buff=0.5)
        self.play(Write(pivot))
        self.wait(1.0)
        self.play(FadeOut(pivot))

        axes = Axes(x_range=(0, 3.3, 1), y_range=(0, 10, 2), width=8, height=5)
        axes.center()
        graph = axes.get_graph(f, x_range=[0, 3.0], color=BLUE, stroke_width=3)
        cap = Text("area under  f(x) = x²  from 0 to 3", font_size=24, color=BLUE)
        cap.to_edge(UP, buff=0.5)
        self.play(ShowCreation(axes), ShowCreation(graph), Write(cap))

        cur, cur_lab = None, None
        for n in [4, 8, 16, 32, 64]:
            rects, total = self.riemann(axes, n, A_INT, B_INT)
            lab = Tex(f"n = {n},   S_n \\approx {total:.3f}", font_size=30)
            lab.to_corner(UR)
            if cur is None:
                self.play(LaggedStartMap(FadeIn, rects, lag_ratio=0.02), Write(lab))
            else:
                self.play(ReplacementTransform(cur, rects),
                          ReplacementTransform(cur_lab, lab))
            cur, cur_lab = rects, lab
            self.wait(0.4)

        lim_tex = Tex(
            r"\int_0^3 x^2\,dx = \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i)\,\Delta x = 9",
            font_size=30)
        lim_tex.to_edge(DOWN, buff=0.6)
        self.play(Write(lim_tex))
        snote = Text("∫  is a stretched  S  for  'sum'", font_size=22, color=GREY_B)
        snote.next_to(lim_tex, DOWN, buff=0.2)
        self.play(Write(snote))
        self.wait(1.5)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(cap), FadeOut(cur),
                  FadeOut(cur_lab), FadeOut(lim_tex), FadeOut(snote))

    # ---------- 6. the Fundamental Theorem of Calculus ----------
    def beat_ftc(self):
        title = Text("The Fundamental Theorem of Calculus", font_size=30, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        axes = Axes(x_range=(0, 3.3, 1), y_range=(0, 10, 2), width=7.5, height=4.6)
        axes.to_edge(LEFT, buff=1.0)
        graph = axes.get_graph(f, x_range=[0, 3.0], color=BLUE, stroke_width=3)
        self.play(ShowCreation(axes), ShowCreation(graph))

        x_tr = ValueTracker(0.01)
        get_x = x_tr.get_value

        def area_poly():
            t = max(0.01, get_x())
            xs = np.linspace(0, t, 60)
            pts = [axes.c2p(x, f(x)) for x in xs] + [axes.c2p(t, 0), axes.c2p(0, 0)]
            p = Polygon(*pts)
            p.set_fill(BLUE_E, 0.5)
            p.set_stroke(width=0)
            return p

        area = always_redraw(area_poly)
        vline = always_redraw(
            lambda: Line(axes.c2p(get_x(), 0), axes.c2p(get_x(), f(get_x())),
                         color=YELLOW, stroke_width=2))
        Flab = Tex(r"F(x) = \int_0^x t^2\,dt", font_size=32)
        Flab.to_corner(UR)
        self.play(FadeIn(area), FadeIn(vline), Write(Flab))
        self.play(x_tr.animate.set_value(3.0), run_time=5, rate_func=linear)

        fact = Tex(r"F(x) = \frac{x^3}{3}, \quad F(3) = 9", font_size=32)
        fact.next_to(Flab, DOWN, buff=0.3)
        self.play(Write(fact))
        self.wait(1.2)
        area.clear_updaters()
        vline.clear_updaters()
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(area), FadeOut(vline),
                  FadeOut(Flab), FadeOut(fact))

        # the insight, on a clean screen
        insight = Tex(r"\frac{dF}{dx} = f(x)", font_size=48, color=YELLOW)
        insight.to_edge(UP, buff=1.5)
        self.play(Write(insight))
        expl = Text("the area grows at a rate equal to the height of the curve",
                    font_size=24, color=GREY_B)
        expl.next_to(insight, DOWN, buff=0.5)
        self.play(Write(expl))
        self.wait(1.8)
        self.play(FadeOut(insight), FadeOut(expl))

        # the inverse relationship
        inv1 = Tex(r"\frac{d}{dx}\int_a^x f(t)\,dt = f(x)", font_size=36)
        inv2 = Tex(r"\int_a^b f(x)\,dx = F(b) - F(a)", font_size=36)
        inv = VGroup(inv1, inv2).arrange(DOWN, buff=0.5)
        inv.to_edge(DOWN, buff=1.8)
        box = SurroundingRectangle(inv, color=GOLD, buff=0.25)
        crown = Text("derivatives and integrals are inverses", font_size=26, color=GREY_B)
        crown.next_to(box, UP, buff=0.25)
        self.play(Write(inv1), Write(inv2), ShowCreation(box), Write(crown))
        self.wait(2.2)
        self.play(FadeOut(title), FadeOut(inv), FadeOut(box), FadeOut(crown))

    # ---------- 7. why it matters / outro ----------
    def beat_outro(self):
        chain = Tex(r"s(t) \;\longrightarrow\; v(t)=s'(t) \;\longrightarrow\; a(t)=v'(t)",
                    font_size=30)
        chain.to_edge(UP, buff=0.8)
        chain_cap = Text("each arrow takes a derivative", font_size=22, color=GREY_B)
        chain_cap.next_to(chain, DOWN, buff=0.25)
        self.play(Write(chain), Write(chain_cap))
        ex = Tex(r"s(t)=t^2 \;\to\; v(t)=2t \;\to\; a(t)=2", font_size=28, color=BLUE)
        ex.next_to(chain_cap, DOWN, buff=0.5)
        self.play(Write(ex))

        app2 = Text("area under velocity  =  distance traveled", font_size=24, color=GREEN)
        app2.next_to(ex, DOWN, buff=0.6)
        self.play(Write(app2))
        app3 = Text("where  f '(x) = 0,  f has a peak or valley", font_size=24, color=YELLOW)
        app3.next_to(app2, DOWN, buff=0.4)
        self.play(Write(app3))
        self.wait(1.6)
        self.play(FadeOut(chain), FadeOut(chain_cap), FadeOut(ex), FadeOut(app2), FadeOut(app3))

        recap = VGroup(
            Text("Limits let us speak of the instant.", font_size=30),
            Text("Derivatives measure change at an instant.", font_size=30),
            Text("Integrals accumulate change.", font_size=30),
        ).arrange(DOWN, buff=0.5)
        self.play(LaggedStart(*[Write(t) for t in recap], lag_ratio=0.7, run_time=3))
        close = Text("Calculus — the language of everything that changes.",
                     font_size=32, color=YELLOW)
        close.next_to(recap, DOWN, buff=0.6)
        self.play(Write(close))
        self.wait(3.0)
        self.play(FadeOut(recap), FadeOut(close))

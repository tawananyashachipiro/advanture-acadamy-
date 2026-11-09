from manim import *

NAVY = "#0F2238"
TEAL = "#2F9E92"
MINT = "#D8F1EC"
SAND = "#FFD27A"
WHITE = "#FFFFFF"


class AcademyIntro(Scene):
    def construct(self):
        self.camera.background_color = NAVY

        eyebrow = Text("LEARN BY EXPLORING", font_size=22, color=TEAL, weight=BOLD)
        title = Text("ADVENTURE ACADEMY", font_size=48, color=WHITE, weight=BOLD)
        subtitle = Text("Every discovery starts with you.", font_size=27, color=SAND)
        intro = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.28)
        intro.move_to(UP * 1.65)

        compass = Circle(radius=0.52, color=TEAL, stroke_width=7)
        needle = Triangle(color=SAND, fill_opacity=1).scale(0.27).rotate(PI / 4)
        needle.move_to(compass.get_center())
        compass_group = VGroup(compass, needle).next_to(intro, DOWN, buff=0.48)

        self.play(FadeIn(eyebrow, shift=UP * 0.2), run_time=0.7)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.play(FadeIn(compass_group, scale=0.8), run_time=0.6)
        self.wait(0.8)

        subjects = [
            "Biology", "Chemistry", "Physics", "Geography",
            "History", "Computer Science", "Business Studies", "Shona",
            "Art & Design", "Mathematics", "Science", "Library",
        ]
        cards = VGroup()
        for subject in subjects:
            card = RoundedRectangle(
                corner_radius=0.12,
                width=3.05,
                height=0.68,
                stroke_color=TEAL,
                stroke_width=2,
                fill_color=MINT,
                fill_opacity=1,
            )
            label = Text(subject, font_size=21, color=NAVY, weight=MEDIUM)
            if label.width > 2.75:
                label.scale_to_fit_width(2.75)
            label.move_to(card.get_center())
            cards.add(VGroup(card, label))

        cards.arrange_in_grid(rows=3, cols=4, buff=(0.22, 0.22))
        cards.scale(0.9).move_to(DOWN * 0.55)
        self.play(FadeOut(compass_group), FadeOut(intro), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.08),
            run_time=2.8,
        )

        footer = Text("Explore • Learn • Create", font_size=23, color=SAND)
        footer.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(footer), run_time=0.6)
        self.wait(2)

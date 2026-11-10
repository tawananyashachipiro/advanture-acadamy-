# Apollo 13 storyboard includes original animated pixel-art scenes.
import json
import os
from pathlib import Path

from manim import *

# Vertical 9:16 canvas for YouTube Shorts.
config.pixel_width = 720
config.pixel_height = 1280
config.frame_width = 4.5
config.frame_height = 8

NAVY = "#0F2238"
TEAL = "#2F9E92"
MINT = "#D8F1EC"
SAND = "#FFD27A"
WHITE = "#FFFFFF"
PALE = "#EAF3F8"


def fit_line(text, size=34, color=WHITE, weight=NORMAL, max_width=3.8):
    mob = Text(str(text), font_size=size, color=color, weight=weight)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def fit_paragraph(text, size=29, color=WHITE, max_width=3.8):
    mob = Paragraph(*str(text).split("\n"), font_size=size, color=color,
                    alignment="center", line_spacing=0.72)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    if mob.height > 3.7:
        mob.scale_to_fit_height(3.7)
    return mob

def pixel_sprite(pattern, palette, pixel=0.11):
    """Build a small, original pixel-art sprite from a character grid."""
    cells = VGroup()
    height = len(pattern)
    for row, line in enumerate(pattern):
        for col, symbol in enumerate(line):
            if symbol == ".":
                continue
            square = Square(side_length=pixel, stroke_width=0)
            square.set_fill(palette[symbol], opacity=1)
            square.move_to([
                (col - (len(line) - 1) / 2) * pixel,
                ((height - 1) / 2 - row) * pixel,
                0,
            ])
            cells.add(square)
    return cells


def apollo_pixel_story(scene, index, step):
    """Animated original pixel-art storytelling for Apollo 13."""
    stars = VGroup(*[
        Dot([((i * 37) % 41) / 10 - 2, ((i * 19) % 67) / 10 - 3.2, 0],
            radius=0.012, color=PALE)
        for i in range(42)
    ])
    heading = fit_line(step["heading"], 25, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 21, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.2).move_to(DOWN * 2.65)
    scene.add(stars)
    scene.play(FadeIn(caption, shift=UP * 0.1), run_time=0.4)

    if index == 1:
        earth = Circle(radius=0.78, color="#2876B8", fill_color="#2876B8", fill_opacity=1)
        earth.move_to(LEFT * 1.25 + DOWN * 0.05)
        moon = pixel_sprite(["...MMMM...", ".MMMMMMMM.", "MMMMMMMMMM",
                             "MMMMMMMMMM", "MMMMMMMMMM", ".MMMMMMMM.", "...MMMM..."],
                            {"M": MINT}, pixel=0.09).move_to(RIGHT * 1.35 + UP * 1.0)
        rocket = pixel_sprite(["....W....", "...WWW...", "...WRW...",
                               "..RRRRR..", "..RWRWR..", "...WWW...",
                               "..B...B..", ".B.....B."],
                              {"W": WHITE, "R": SAND, "B": TEAL},
                              pixel=0.11).move_to(LEFT * 1.2 + DOWN * 1.0)
        date = fit_line("11 APRIL 1970", 22, TEAL, BOLD).move_to(UP * 2.0)
        scene.play(FadeIn(earth), FadeIn(moon), FadeIn(rocket), FadeIn(date), run_time=0.7)
        scene.play(rocket.animate.shift(RIGHT * 1.5 + UP * 1.7), run_time=1.8, rate_func=smooth)
        scene.play(FadeOut(earth), FadeOut(moon), FadeOut(rocket), FadeOut(date), run_time=0.4)

    elif index == 2:
        module = VGroup(
            Rectangle(width=1.25, height=0.72, fill_color="#8299A8",
                      fill_opacity=1, stroke_color=WHITE),
            Rectangle(width=0.55, height=0.9, fill_color="#38566D",
                      fill_opacity=1, stroke_color=TEAL).shift(RIGHT * 0.88),
            Rectangle(width=0.55, height=0.38, fill_color="#17334C",
                      fill_opacity=1, stroke_color=SAND).shift(LEFT * 0.9),
        ).move_to(UP * 1.0)
        warning = VGroup(
            Triangle(color=SAND, fill_color=SAND, fill_opacity=1).scale(0.48),
            Text("!", font_size=34, color=NAVY, weight=BOLD)
        ).move_to(DOWN * 0.1)
        alert = fit_line("OXYGEN SYSTEM ALERT", 23, SAND, BOLD).move_to(DOWN * 0.9)
        desk = RoundedRectangle(width=3.8, height=0.8, corner_radius=0.1,
                                stroke_color=TEAL, fill_color="#17334C", fill_opacity=1)
        desk.move_to(DOWN * 1.8)
        screens = VGroup(*[
            Rectangle(width=0.55, height=0.32, stroke_color=TEAL,
                      fill_color="#245A70", fill_opacity=1).move_to([x, -1.8, 0])
            for x in [-1.25, -0.42, 0.42, 1.25]
        ])
        operators = VGroup(*[
            pixel_sprite([".WWW.", "WCCCW", ".WWW.", "..W..", ".W.W."],
                         {"W": WHITE, "C": TEAL}, pixel=0.07).move_to([x, -1.1, 0])
            for x in [-1.0, 0, 1.0]
        ])
        scene.play(FadeIn(module), FadeIn(warning), FadeIn(alert), run_time=0.75)
        scene.play(Indicate(warning, color=SAND, scale_factor=1.15), run_time=0.7)
        scene.play(FadeIn(desk), FadeIn(screens), FadeIn(operators), run_time=0.65)
        scene.wait(0.35)
        scene.play(FadeOut(module), FadeOut(warning), FadeOut(alert),
                   FadeOut(desk), FadeOut(screens), FadeOut(operators), run_time=0.4)

    else:
        earth = Circle(radius=0.92, color="#2876B8", fill_color="#2876B8",
                       fill_opacity=1).move_to(UP * 1.05)
        lunar_module = pixel_sprite(["..WWW..", ".WSSSW.", "WWSSSWW",
                                     "..WWW..", ".B...B."],
                                    {"W": WHITE, "S": "#A8C8D8", "B": TEAL},
                                    pixel=0.12).move_to(LEFT * 1.15 + DOWN * 0.1)
        crew = VGroup(*[
            pixel_sprite([".WWW.", "WCCCW", ".WWW.", "..W..", ".W.W."],
                         {"W": WHITE, "C": TEAL}, pixel=0.07).move_to([x, -0.85, 0])
            for x in [-1.0, 0, 1.0]
        ])
        label = fit_line("AQUARIUS • CREW LIFeboat".upper(), 19, TEAL, BOLD)
        label.move_to(DOWN * 1.55)
        scene.play(FadeIn(earth), FadeIn(lunar_module), FadeIn(crew), FadeIn(label), run_time=0.7)
        scene.play(lunar_module.animate.shift(RIGHT * 1.2 + DOWN * 0.25),
                   run_time=1.3, rate_func=smooth)
        ocean = VGroup(*[
            Line(LEFT * 1.8 + DOWN * (1.3 + i * 0.13),
                 RIGHT * 1.8 + DOWN * (1.3 + i * 0.13), color=TEAL, stroke_width=2)
            for i in range(3)
        ])
        capsule = pixel_sprite(["..WWW..", ".WSSSW.", "WWSSSWW", "..WWW.."],
                               {"W": WHITE, "S": "#A8C8D8"},
                               pixel=0.09).move_to(UP * 0.15)
        parachutes = VGroup(*[
            Arc(radius=0.23, angle=PI, color=WHITE, stroke_width=3).move_to([x, 0.75, 0])
            for x in [-0.45, 0, 0.45]
        ])
        splash = fit_line("17 APRIL 1970 • SAFE SPLASHDOWN", 19, SAND, BOLD, max_width=4.0)
        splash.move_to(DOWN * 1.85)
        scene.play(FadeOut(earth), FadeOut(lunar_module), FadeOut(crew), FadeOut(label),
                   FadeIn(ocean), FadeIn(capsule), FadeIn(parachutes), run_time=0.55)
        scene.play(capsule.animate.shift(DOWN * 0.65),
                   parachutes.animate.shift(DOWN * 0.5), run_time=1.1, rate_func=smooth)
        scene.play(FadeIn(splash), run_time=0.45)
        scene.play(FadeOut(ocean), FadeOut(capsule), FadeOut(parachutes), FadeOut(splash), run_time=0.4)

    scene.play(FadeOut(caption), FadeOut(stars), run_time=0.3)


class AcademyLessonShort(Scene):
    def construct(self):
        lesson_path = os.environ.get("ACADEMY_LESSON_FILE", "creator-studio/lessons/active-lesson.json")
        lesson = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
        self.camera.background_color = NAVY

        brand = fit_line("ADVENTURE OF EDUCATION", 20, TEAL, BOLD, 4.0)
        brand.to_edge(UP, buff=0.42)
        self.add(brand)

        if lesson.get("title", "").startswith("Apollo 13:"):
            # A short visual cold-open: original pixel-art rocket and Moon.
            # Keep it simple and locally rendered; no stock footage or paid assets.
            rocket = pixel_sprite([
                "....W....",
                "...WWW...",
                "...WRW...",
                "..RRRRR..",
                "..RWRWR..",
                "..RRRRR..",
                "...B.B...",
                "..B...B..",
                ".B.....B.",
            ], {"W": WHITE, "R": SAND, "B": TEAL}, pixel=0.105)
            moon = pixel_sprite([
                "...MMMM...",
                ".MMMMMMMM.",
                "MMMMMMMMMM",
                "MMMMMMMMMM",
                "MMMMMMMMMM",
                ".MMMMMMMM.",
                "...MMMM...",
            ], {"M": MINT}, pixel=0.105)
            rocket.move_to(LEFT * 0.72 + UP * 0.55)
            moon.move_to(RIGHT * 0.95 + UP * 0.55)
            cold_open = fit_paragraph(
                "A MOON MISSION. A SUDDEN EMERGENCY. THREE ASTRONAUTS NEED A WAY HOME.",
                31, SAND, max_width=4.0
            )
            cold_open.move_to(DOWN * 1.15)
            self.play(FadeIn(rocket), FadeIn(moon), run_time=0.55)
            self.play(rocket.animate.shift(UP * 0.18), FadeIn(cold_open), run_time=0.75)
            self.wait(1.7)
            self.play(FadeOut(rocket), FadeOut(moon), FadeOut(cold_open), run_time=0.35)

        title = fit_paragraph(lesson["title"], 38, WHITE)
        title.move_to(UP * 1.05)
        subject = fit_line(lesson["subject"].upper() + " • " + lesson["level"], 19, SAND, BOLD)
        subject.next_to(title, DOWN, buff=0.48)
        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subject), run_time=1.1)
        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(subject), run_time=0.35)

        hook_label = fit_line("YOUR MISSION", 25, TEAL, BOLD)
        hook = fit_paragraph(lesson["hook"], 38, SAND)
        group = VGroup(hook_label, hook).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(group, shift=UP * 0.25), run_time=0.8)
        self.wait(2.7)
        self.play(FadeOut(group), run_time=0.35)

        concept_label = fit_line("THE BIG IDEA", 24, TEAL, BOLD)
        concept = fit_paragraph(lesson["concept"], 30, WHITE)
        group = VGroup(concept_label, concept).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(group), run_time=0.8)
        self.wait(3.7)
        self.play(FadeOut(group), run_time=0.4)

        photo_dir = Path(os.environ.get("ACADEMY_ASSET_DIR", "creator-studio/assets/apollo-13"))
        is_apollo = lesson.get("title", "").startswith("Apollo 13:")
        for index, step in enumerate(lesson["steps"], start=1):
            if is_apollo:
                apollo_pixel_story(self, index, step)
            else:
                number = fit_line(f"DISCOVERY {index}", 23, TEAL, BOLD)
                heading = fit_paragraph(step["heading"], 38, SAND)
                body = fit_paragraph(step["body"], 30, WHITE)
                card = VGroup(number, heading, body).arrange(DOWN, buff=0.45).move_to(ORIGIN)
                self.play(FadeIn(card, shift=UP * 0.18), run_time=0.7)
                self.wait(3.5)
                self.play(FadeOut(card), run_time=0.35)

        challenge = fit_line("PAUSE & PLAY", 25, TEAL, BOLD)
        question = fit_paragraph(lesson["question"], 34, SAND)
        choices = VGroup(*[
            fit_paragraph(f"{chr(65+i)}. {option}", 26, WHITE)
            for i, option in enumerate(lesson["options"])
        ]).arrange(DOWN, buff=0.25)
        quiz = VGroup(challenge, question, choices).arrange(DOWN, buff=0.42).move_to(ORIGIN)
        self.play(FadeIn(quiz), run_time=0.8)
        self.wait(5.0)
        self.play(FadeOut(quiz), run_time=0.4)

        answer = fit_line("ANSWER REVEALED", 24, TEAL, BOLD)
        correct = fit_paragraph(lesson["options"][lesson["answer_index"]], 42, SAND)
        why = fit_paragraph(lesson["explanation"], 29, WHITE)
        reveal = VGroup(answer, correct, why).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(reveal, scale=0.96), run_time=0.8)
        self.wait(3.8)
        self.play(FadeOut(reveal), run_time=0.4)

        if is_apollo:
            end_card = VGroup(
                fit_line("THREE ASTRONAUTS. ONE SAFE RETURN.", 23, SAND, BOLD, max_width=4.0),
                fit_line("PACIFIC OCEAN • 17 APRIL 1970", 20, WHITE, BOLD),
            ).arrange(DOWN, buff=0.28).move_to(UP * 0.6)
            self.play(FadeIn(end_card), run_time=0.6)
            self.wait(0.7)
            self.play(FadeOut(end_card), run_time=0.35)
        outro = VGroup(
            fit_line("MISSION COMPLETE!", 32, SAND, BOLD),
            fit_paragraph("Explore • Learn • Create", 30, WHITE),
            fit_paragraph("Try the lesson and quiz at Adventure Academy.", 25, TEAL),
        ).arrange(DOWN, buff=0.48).move_to(ORIGIN)
        self.play(FadeIn(outro), run_time=0.8)
        self.wait(2.5)

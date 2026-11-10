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
        apollo_photos = [
            photo_dir / "launch.jpg",
            photo_dir / "mission-control.jpg",
            photo_dir / "earth-return.jpg",
        ] if lesson.get("title", "").startswith("Apollo 13:") else []
        for index, step in enumerate(lesson["steps"], start=1):
            if index <= len(apollo_photos) and apollo_photos[index - 1].exists():
                photo = ImageMobject(str(apollo_photos[index - 1]))
                photo.scale(min(4.05 / photo.width, 4.45 / photo.height))
                photo.move_to(UP * 0.55)
                frame = SurroundingRectangle(photo, color=TEAL, buff=0.07, stroke_width=2)
                heading = fit_line(step["heading"], 25, SAND, BOLD, max_width=4.0)
                body = fit_paragraph(step["body"], 22, WHITE, max_width=4.0)
                caption = VGroup(heading, body).arrange(DOWN, buff=0.22)
                caption.move_to(DOWN * 2.55)
                self.play(FadeIn(photo), Create(frame), FadeIn(caption, shift=UP * 0.12), run_time=0.65)
                self.play(photo.animate.scale(1.035), run_time=2.2)
                self.play(FadeOut(photo), FadeOut(frame), FadeOut(caption), run_time=0.4)
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

        splashdown = photo_dir / "splashdown.jpg"
        if lesson.get("title", "").startswith("Apollo 13:") and splashdown.exists():
            photo = ImageMobject(str(splashdown))
            photo.scale(min(4.15 / photo.width, 4.6 / photo.height))
            photo.move_to(UP * 0.45)
            frame = SurroundingRectangle(photo, color=TEAL, buff=0.07, stroke_width=2)
            end_caption = VGroup(
                fit_line("17 APRIL 1970", 24, SAND, BOLD),
                fit_line("ALL THREE ASTRONAUTS HOME SAFELY", 21, WHITE, BOLD, max_width=4.0),
            ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.65)
            self.play(FadeIn(photo), Create(frame), FadeIn(end_caption), run_time=0.8)
            self.play(photo.animate.scale(1.035), run_time=2.0)
            self.play(FadeOut(photo), FadeOut(frame), FadeOut(end_caption), run_time=0.35)
        outro = VGroup(
            fit_line("MISSION COMPLETE!", 32, SAND, BOLD),
            fit_paragraph("Explore • Learn • Create", 30, WHITE),
            fit_paragraph("Try the lesson and quiz at Adventure Academy.", 25, TEAL),
        ).arrange(DOWN, buff=0.48).move_to(ORIGIN)
        self.play(FadeIn(outro), run_time=0.8)
        self.wait(2.5)

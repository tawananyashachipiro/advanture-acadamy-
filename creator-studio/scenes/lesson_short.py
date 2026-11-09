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


class AcademyLessonShort(Scene):
    def construct(self):
        lesson_path = os.environ.get("ACADEMY_LESSON_FILE", "creator-studio/lessons/active-lesson.json")
        lesson = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
        self.camera.background_color = NAVY

        brand = fit_line("ADVENTURE ACADEMY", 20, TEAL, BOLD, 4.0)
        brand.to_edge(UP, buff=0.42)
        self.add(brand)

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

        for index, step in enumerate(lesson["steps"], start=1):
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

        outro = VGroup(
            fit_line("MISSION COMPLETE!", 32, SAND, BOLD),
            fit_paragraph("Explore • Learn • Create", 30, WHITE),
            fit_paragraph("Try the lesson and quiz at Adventure Academy.", 25, TEAL),
        ).arrange(DOWN, buff=0.48).move_to(ORIGIN)
        self.play(FadeIn(outro), run_time=0.8)
        self.wait(2.5)

# Apollo 13 storyboard includes original animated pixel-art scenes.
import json
import math
import os
import textwrap
from pathlib import Path

from manim import *

# Vertical 9:16 canvas for YouTube Shorts.
config.pixel_width = 720
config.pixel_height = 1920
config.frame_rate = 30
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
    # Wrap long narration/lesson copy before creating the text object. A single
    # unbroken line gets scaled down until it fits, making mobile captions tiny.
    wrap_width = max(18, int(42 * 29 / max(1, size)))
    lines = []
    for paragraph in str(text).splitlines() or [""]:
        lines.extend(textwrap.wrap(paragraph, width=wrap_width) or [""])
    mob = Paragraph(*lines, font_size=size, color=color,
                    alignment="center", line_spacing=0.82)
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
    body = fit_paragraph(step["body"], 28, WHITE, max_width=4.0)
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



def great_zimbabwe_pixel_story(scene, index, step):
    """Original pixel-art scenes for the Great Zimbabwe history Short."""
    stars = VGroup(*[
        Dot([((i * 29) % 43) / 11 - 2, ((i * 17) % 61) / 10 - 3.0, 0],
            radius=0.012, color=PALE)
        for i in range(36)
    ])
    heading = fit_line(step["heading"], 25, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 21, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.2).move_to(DOWN * 2.65)
    scene.add(stars)
    scene.play(FadeIn(caption, shift=UP * 0.1), run_time=0.4)

    stone_palette = {"S": "#B9A58A", "D": "#786A59", "L": "#E0D0B8"}
    wall_pattern = [
        "SSSSSSSSSSSSSSSS",
        "DSSSDSSSDSSSDSSS",
        "SSSSSSSSSSSSSSSS",
        "SSSDSSSDSSSDSSSS",
        "SSSSSSSSSSSSSSSS",
        "DSSSDSSSDSSSDSSS",
    ]

    if index == 1:
        hill = Polygon(
            [-2.0, -0.9, 0], [-1.2, 0.15, 0], [-0.45, 0.85, 0],
            [0.3, 0.35, 0], [1.25, 0.9, 0], [2.0, -0.75, 0],
            color="#496C54", fill_color="#496C54", fill_opacity=1
        )
        hill.shift(UP * 0.25)
        wall = pixel_sprite(wall_pattern, stone_palette, pixel=0.105)
        wall.move_to(DOWN * 0.45)
        tower = pixel_sprite(
            ["....LL....", "...LLLL...", "..LLLLLL..", ".LLLLLLLL.",
             "LLLLLLLLLL", "LLLLLLLLLL"],
            {"L": "#E0D0B8", "S": "#B9A58A"}, pixel=0.085
        ).move_to(RIGHT * 1.05 + UP * 0.45)
        bird = pixel_sprite(
            ["..WW..", ".WWWW.", "WW.WW.", "..WW..", ".W..W."],
            {"W": SAND}, pixel=0.085
        ).move_to(LEFT * 1.15 + UP * 1.25)
        date = fit_line("SOUTHERN AFRICA • MEDIEVAL ERA", 18, TEAL, BOLD, 4.0)
        date.move_to(UP * 2.0)
        scene.play(FadeIn(hill), FadeIn(wall), FadeIn(tower), FadeIn(bird),
                   FadeIn(date), run_time=0.8)
        scene.play(wall.animate.shift(RIGHT * 0.18),
                   tower.animate.shift(UP * 0.12), run_time=1.0, rate_func=smooth)
        scene.play(FadeOut(hill), FadeOut(wall), FadeOut(tower),
                   FadeOut(bird), FadeOut(date), run_time=0.45)

    elif index == 2:
        wall = pixel_sprite(wall_pattern, stone_palette, pixel=0.15)
        wall.move_to(UP * 0.45)
        arch = Arc(radius=0.65, angle=PI, color="#E0D0B8", stroke_width=9)
        arch.move_to(UP * 0.9)
        label = fit_line("GRANITE • NO MORTAR", 22, TEAL, BOLD)
        label.move_to(DOWN * 1.15)
        scene.play(FadeIn(wall), Create(arch), run_time=0.85)
        scene.play(Indicate(wall, color=SAND, scale_factor=1.04), run_time=0.8)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(wall), FadeOut(arch), FadeOut(label), run_time=0.45)

    else:
        ocean = VGroup(*[
            Line(LEFT * 1.9 + DOWN * (0.65 + i * 0.16),
                 RIGHT * 1.9 + DOWN * (0.65 + i * 0.16),
                 color=TEAL, stroke_width=2)
            for i in range(4)
        ])
        hull = Polygon(
            [-1.1, 0.05, 0], [1.15, 0.05, 0], [0.72, -0.35, 0],
            [-0.65, -0.35, 0], color=SAND, fill_color=SAND, fill_opacity=1
        )
        sail = Polygon(
            [-0.12, 0.1, 0], [-0.12, 1.25, 0], [0.75, 0.1, 0],
            color=WHITE, fill_color=WHITE, fill_opacity=1
        )
        mast = Line([-0.12, -0.05, 0], [-0.12, 1.35, 0], color=SAND, stroke_width=4)
        beads = VGroup(*[
            Circle(radius=0.10, color=c, fill_color=c, fill_opacity=1).move_to([x, y, 0])
            for x, y, c in [
                (-1.0, 1.1, TEAL), (-0.65, 1.45, SAND), (0.95, 1.2, "#C77B55"),
                (1.25, 0.8, MINT), (0.65, 1.65, SAND)
            ]
        ])
        route = fit_line("GOLD • BEADS • INDIAN OCEAN TRADE", 18, SAND, BOLD, 4.0)
        route.move_to(DOWN * 1.35)
        ship = VGroup(hull, sail, mast)
        scene.play(FadeIn(ocean), FadeIn(ship), FadeIn(beads), run_time=0.8)
        scene.play(ship.animate.shift(RIGHT * 0.45), beads.animate.shift(LEFT * 0.12),
                   run_time=1.25, rate_func=smooth)
        scene.play(FadeIn(route), run_time=0.45)
        scene.play(FadeOut(ocean), FadeOut(ship), FadeOut(beads), FadeOut(route), run_time=0.45)

    scene.play(FadeOut(caption), FadeOut(stars), run_time=0.3)


def antikythera_pixel_story(scene, index, step):
    """Original pixel-art scenes for the Antikythera Mechanism history Short."""
    stars = VGroup(*[
        Dot([((i * 31) % 41) / 10 - 2, ((i * 17) % 59) / 10 - 3.0, 0],
            radius=0.012, color=PALE)
        for i in range(34)
    ])
    heading = fit_line(step["heading"], 25, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 21, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.2).move_to(DOWN * 2.65)
    scene.add(stars)
    scene.play(FadeIn(caption, shift=UP * 0.1), run_time=0.4)

    bronze = "#B98248"
    dark_bronze = "#68452F"
    if index == 1:
        sea = Rectangle(width=4.3, height=3.3, fill_color="#123B59",
                        fill_opacity=1, stroke_width=0).move_to(UP * 0.45)
        waves = VGroup(*[
            Arc(radius=0.28 + i * 0.05, angle=PI * 0.8, color=TEAL,
                stroke_width=2).move_to([x, y, 0])
            for i, (x, y) in enumerate([(-1.4, 1.5), (-0.6, 1.15),
                                         (0.5, 1.55), (1.25, 1.0)])
        ])
        hull = Polygon([-1.45, -0.25, 0], [1.35, -0.25, 0],
                       [0.9, -0.75, 0], [-0.9, -0.75, 0],
                       color=dark_bronze, fill_color=dark_bronze, fill_opacity=1)
        mast = Line([0, -0.2, 0], [0, 0.95, 0], color=SAND, stroke_width=4)
        fragment = VGroup(*[
            Square(side_length=0.28, fill_color=bronze, fill_opacity=1,
                   stroke_color=SAND).move_to([x, y, 0])
            for x, y in [(-0.45, -1.0), (0.1, -1.05), (0.58, -0.95)]
        ])
        label = fit_line("ANTIKYTHERA • 1901", 20, SAND, BOLD)
        label.move_to(UP * 1.95)
        scene.play(FadeIn(sea), FadeIn(waves), FadeIn(hull), Create(mast),
                   FadeIn(fragment), FadeIn(label), run_time=0.85)
        scene.play(fragment.animate.shift(UP * 0.18), run_time=0.7, rate_func=smooth)
        scene.play(FadeOut(sea), FadeOut(waves), FadeOut(hull), FadeOut(mast),
                   FadeOut(fragment), FadeOut(label), run_time=0.45)

    elif index == 2:
        gear_a = Circle(radius=0.78, color=bronze, stroke_width=8).move_to(LEFT * 0.72 + UP * 0.55)
        gear_b = Circle(radius=0.48, color=SAND, stroke_width=7).move_to(RIGHT * 0.72 + UP * 0.55)
        spokes_a = VGroup(*[
            Line(gear_a.get_center(), gear_a.get_center() + 0.68 * np.array([np.cos(a), np.sin(a), 0]),
                 color=bronze, stroke_width=5)
            for a in np.linspace(0, TAU, 10, endpoint=False)
        ])
        spokes_b = VGroup(*[
            Line(gear_b.get_center(), gear_b.get_center() + 0.4 * np.array([np.cos(a), np.sin(a), 0]),
                 color=SAND, stroke_width=4)
            for a in np.linspace(0, TAU, 8, endpoint=False)
        ])
        hub_a = Dot(gear_a.get_center(), radius=0.12, color=SAND)
        hub_b = Dot(gear_b.get_center(), radius=0.1, color=bronze)
        label = fit_line("ABOUT 30 TOOTHED GEARS", 20, TEAL, BOLD)
        label.move_to(DOWN * 1.0)
        scene.play(Create(gear_a), Create(gear_b), FadeIn(spokes_a), FadeIn(spokes_b),
                   FadeIn(hub_a), FadeIn(hub_b), run_time=0.9)
        scene.play(Rotate(VGroup(spokes_a, hub_a), angle=PI / 3, about_point=gear_a.get_center()),
                   Rotate(VGroup(spokes_b, hub_b), angle=-PI / 2, about_point=gear_b.get_center()),
                   run_time=1.2, rate_func=smooth)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(gear_a), FadeOut(gear_b), FadeOut(spokes_a),
                   FadeOut(spokes_b), FadeOut(hub_a), FadeOut(hub_b),
                   FadeOut(label), run_time=0.45)

    else:
        dial = Circle(radius=1.12, color=bronze, stroke_width=8).move_to(UP * 0.55)
        ring = Circle(radius=0.82, color=SAND, stroke_width=3).move_to(dial.get_center())
        sun = Circle(radius=0.22, color=SAND, fill_color=SAND, fill_opacity=1).move_to(LEFT * 0.48 + UP * 0.55)
        moon = Circle(radius=0.2, color=MINT, fill_color=MINT, fill_opacity=1).move_to(RIGHT * 0.48 + UP * 0.55)
        hand = Line(dial.get_center(), dial.get_center() + UP * 0.88,
                    color=WHITE, stroke_width=5)
        ticks = VGroup(*[
            Line(dial.get_center() + 0.9 * np.array([np.cos(a), np.sin(a), 0]),
                 dial.get_center() + 1.02 * np.array([np.cos(a), np.sin(a), 0]),
                 color=WHITE, stroke_width=3)
            for a in np.linspace(0, TAU, 12, endpoint=False)
        ])
        label = fit_line("SUN • MOON • ECLIPSE CYCLES", 19, SAND, BOLD, 4.0)
        label.move_to(DOWN * 1.25)
        scene.play(Create(dial), Create(ring), FadeIn(ticks), FadeIn(sun),
                   FadeIn(moon), Create(hand), run_time=0.85)
        scene.play(Rotate(hand, angle=PI * 0.7, about_point=dial.get_center()),
                   FadeIn(label), run_time=1.2, rate_func=smooth)
        scene.play(FadeOut(dial), FadeOut(ring), FadeOut(ticks), FadeOut(sun),
                   FadeOut(moon), FadeOut(hand), FadeOut(label), run_time=0.45)

    scene.play(FadeOut(caption), FadeOut(stars), run_time=0.3)




def lightning_physics_story(scene, index, step):
    """Photo-led, animated lightning explainer with clear, sustained visuals."""
    asset_dir = Path(os.environ.get("ACADEMY_ASSET_DIR", "creator-studio/assets/lightning"))
    photo_path = asset_dir / "lightning-noaa.jpg"
    if not photo_path.exists():
        raise FileNotFoundError(f"Required lightning photo missing: {photo_path}")

    photo = ImageMobject(str(photo_path))
    photo.scale_to_fit_width(3.95)
    if photo.height > 3.5:
        photo.scale_to_fit_height(3.5)
    photo.move_to(UP * 0.95)

    photo_frame = SurroundingRectangle(photo, color=TEAL, buff=0.07, stroke_width=3)
    heading = fit_line(step["heading"], 24, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 28, WHITE, max_width=3.95)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.16).move_to(DOWN * 2.55)

    scene.play(FadeIn(photo, scale=1.03), Create(photo_frame), run_time=0.9)
    scene.play(FadeIn(caption, shift=UP * 0.15), run_time=0.65)
    scene.wait(1.1)

    if index == 1:
        label = fit_line("INSIDE THE STORM CLOUD", 20, TEAL, BOLD)
        label.move_to(UP * 3.0)
        cloud = VGroup(
            Circle(radius=0.62, color=PALE, fill_color="#7893A8", fill_opacity=1).shift(LEFT * 0.55),
            Circle(radius=0.82, color=PALE, fill_color="#7893A8", fill_opacity=1).shift(UP * 0.18),
            Circle(radius=0.58, color=PALE, fill_color="#7893A8", fill_opacity=1).shift(RIGHT * 0.58),
            RoundedRectangle(width=2.15, height=0.55, corner_radius=0.2,
                             color=PALE, fill_color="#7893A8", fill_opacity=1).shift(DOWN * 0.35),
        ).scale(0.72).move_to(UP * 1.0)
        positive = VGroup(*[
            Text("+", font_size=34, color=SAND, weight=BOLD).move_to([x, y, 0])
            for x, y in [(-0.72, 1.55), (0, 1.8), (0.7, 1.55), (0.25, 1.15)]
        ])
        negative = VGroup(*[
            Text("−", font_size=36, color=TEAL, weight=BOLD).move_to([x, y, 0])
            for x, y in [(-0.7, 0.35), (0, 0.2), (0.7, 0.38), (0.25, 0.65)]
        ])
        ice = VGroup(*[
            Square(side_length=0.14, color=MINT, fill_color=MINT,
                   fill_opacity=1).rotate(PI / 4).move_to([x, y, 0])
            for x, y in [(-1.25, 0.9), (-0.45, 0.8), (0.55, 0.95), (1.2, 0.75)]
        ])
        arrows = VGroup(*[
            Arrow([x, 0.55, 0], [x + 0.18, 1.12, 0], color=TEAL,
                  buff=0, stroke_width=3)
            for x in [-0.85, 0.0, 0.85]
        ])
        scene.play(FadeOut(photo), FadeOut(photo_frame), FadeIn(cloud), FadeIn(label), run_time=0.65)
        scene.play(FadeIn(ice), FadeIn(arrows), run_time=0.55)
        scene.play(FadeIn(positive), FadeIn(negative), run_time=0.65)
        scene.play(Indicate(positive, color=SAND), Indicate(negative, color=TEAL), run_time=0.8)
        scene.wait(0.9)
        scene.play(FadeOut(cloud), FadeOut(ice), FadeOut(arrows), FadeOut(positive),
                   FadeOut(negative), FadeOut(label), run_time=0.5)

    elif index == 2:
        bolt = Polygon(
            [-0.1, 2.2, 0], [0.35, 2.2, 0], [0.02, 1.35, 0],
            [0.48, 1.35, 0], [-0.35, 0.1, 0], [-0.16, 0.95, 0],
            [-0.58, 0.95, 0], color=SAND, fill_color=SAND,
            fill_opacity=1, stroke_width=2
        )
        branches = VGroup(
            Line([-0.05, 1.5, 0], [-1.05, 0.8, 0], color=WHITE, stroke_width=5),
            Line([0.12, 1.2, 0], [1.0, 0.35, 0], color=WHITE, stroke_width=5),
            Line([-0.24, 0.72, 0], [-0.9, 0.12, 0], color=WHITE, stroke_width=4),
        )
        tag = fit_line("A REAL LIGHTNING FLASH", 22, SAND, BOLD)
        tag.move_to(DOWN * 0.95)
        scene.play(FadeOut(photo_frame), photo.animate.scale(1.18).move_to(UP * 0.85),
                   run_time=0.8)
        scene.play(Create(bolt), run_time=0.55)
        scene.play(Create(branches), run_time=0.6)
        scene.play(Flash(bolt.get_center(), color=WHITE, flash_radius=1.15),
                   Indicate(bolt, color=WHITE, scale_factor=1.12), run_time=0.7)
        scene.play(FadeIn(tag), run_time=0.45)
        scene.wait(1.1)
        scene.play(FadeOut(photo), FadeOut(bolt), FadeOut(branches), FadeOut(tag), run_time=0.5)

    else:
        bolt = Polygon(
            [-0.1, 2.15, 0], [0.35, 2.15, 0], [0.02, 1.3, 0],
            [0.48, 1.3, 0], [-0.35, 0.05, 0], [-0.16, 0.9, 0],
            [-0.58, 0.9, 0], color=SAND, fill_color=SAND,
            fill_opacity=1, stroke_width=2
        )
        waves = VGroup(*[
            Arc(radius=0.42 + i * 0.28, angle=PI * 0.82, color=TEAL,
                stroke_width=5).move_to([0.18, 0.75, 0])
            for i in range(4)
        ])
        light_label = fit_line("FLASH: LIGHT REACHES YOU FIRST", 18, SAND, BOLD, 4.1)
        sound_label = fit_line("THUNDER: SOUND ARRIVES LATER", 18, TEAL, BOLD, 4.1)
        light_label.move_to(DOWN * 1.0)
        sound_label.move_to(DOWN * 1.55)
        scene.play(FadeIn(bolt), run_time=0.5)
        scene.play(Flash(bolt.get_center(), color=WHITE, flash_radius=1.1), run_time=0.5)
        scene.play(Create(waves), run_time=1.0)
        scene.play(waves.animate.scale(1.16), FadeIn(light_label), run_time=0.8)
        scene.play(FadeIn(sound_label), run_time=0.5)
        scene.wait(1.0)
        scene.play(FadeOut(bolt), FadeOut(waves), FadeOut(light_label),
                   FadeOut(sound_label), run_time=0.5)

    scene.play(FadeOut(caption), run_time=0.4)




def hubble_pixel_story(scene, index, step):
    """Original pixel-art scenes for Hubble's first in-orbit repair."""
    stars = VGroup(*[
        Dot([((i * 31) % 41) / 10 - 2, ((i * 17) % 59) / 10 - 3.0, 0],
            radius=0.012, color=PALE)
        for i in range(38)
    ])
    heading = fit_line(step["heading"], 25, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 21, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.2).move_to(DOWN * 2.55)
    scene.add(stars)
    scene.play(FadeIn(caption, shift=UP * 0.1), run_time=0.4)

    if index == 1:
        mirror = pixel_sprite(
            ["....SSSS....", "...SSSSSS...", "..SSSSSSSS..",
             ".SSSSSSSSSS.", "SSSSSSSSSSSS"],
            {"S": "#C9D8E5"}, pixel=0.12
        ).move_to(UP * 0.78)
        incoming = VGroup(*[
            Line([x, 2.35, 0], [x, 1.15, 0], color=SAND, stroke_width=3)
            for x in [-0.82, 0, 0.82]
        ])
        foci = VGroup(
            Dot(LEFT * 0.36 + DOWN * 0.12, radius=0.09, color=TEAL),
            Dot(RIGHT * 0.36 + DOWN * 0.12, radius=0.09, color=TEAL)
        )
        blur = VGroup(*[
            Circle(radius=0.14 + i * 0.09, color=WHITE, stroke_width=2)
            .move_to(DOWN * 0.12)
            for i in range(3)
        ])
        label = fit_line("2.2 MICRONS TOO FLAT", 21, TEAL, BOLD, 4.0)
        label.move_to(DOWN * 1.25)
        scene.play(FadeIn(incoming), FadeIn(mirror), run_time=0.75)
        scene.play(FadeIn(foci), FadeIn(blur), run_time=0.65)
        scene.play(Indicate(mirror, color=SAND), FadeIn(label), run_time=0.75)
        scene.play(FadeOut(incoming), FadeOut(mirror), FadeOut(foci),
                   FadeOut(blur), FadeOut(label), run_time=0.45)

    elif index == 2:
        body_sprite = pixel_sprite(
            ["..BBBBBBBB..", "BBBBBBBBBBBB", "..BBBBBBBB.."],
            {"B": "#DCE6EF"}, pixel=0.09
        ).move_to(RIGHT * 0.45 + UP * 0.78)
        left_panel = pixel_sprite(
            ["PPPPPP", "LLLLLL", "PPPPPP", "LLLLLL"],
            {"P": "#1D5C7A", "L": "#72C9D8"}, pixel=0.12
        ).move_to(LEFT * 0.88 + UP * 0.78)
        right_panel = pixel_sprite(
            ["PPPPPP", "LLLLLL", "PPPPPP", "LLLLLL"],
            {"P": "#1D5C7A", "L": "#72C9D8"}, pixel=0.12
        ).move_to(RIGHT * 1.75 + UP * 0.78)
        telescope = VGroup(body_sprite, left_panel, right_panel)
        shuttle = pixel_sprite(
            ["....WW....", "...WWWW...", "WWWWWWWWWW",
             ".WWWWWWWW.", "..W....W.."],
            {"W": WHITE}, pixel=0.075
        ).move_to(UP * 2.0 + LEFT * 0.1)
        astronaut = pixel_sprite(
            ["..WWW..", ".WSSSW.", "WSSSSSW", ".WWWWW.",
             "..W.W..", ".W...W."],
            {"W": WHITE, "S": SAND}, pixel=0.11
        ).move_to(LEFT * 1.25 + DOWN * 0.12)
        arm = Line(astronaut.get_right(), telescope.get_left(),
                   color=TEAL, stroke_width=4)
        label = fit_line("STS-61 • FIVE SPACEWALKS", 20, SAND, BOLD, 4.0)
        label.move_to(DOWN * 1.35)
        scene.play(FadeIn(shuttle), FadeIn(telescope), FadeIn(astronaut),
                   Create(arm), run_time=0.85)
        scene.play(astronaut.animate.shift(RIGHT * 0.28), run_time=0.9,
                   rate_func=smooth)
        scene.play(Indicate(telescope, color=SAND), FadeIn(label), run_time=0.7)
        scene.play(FadeOut(shuttle), FadeOut(telescope), FadeOut(astronaut),
                   FadeOut(arm), FadeOut(label), run_time=0.45)

    else:
        telescope = pixel_sprite(
            ["....BBBBBBBB....", "...BBBBBBBBBB...",
             "BBBBBBBBBBBBBBBB", "...BBBBBBBBBB...",
             "....BBBBBBBB...."],
            {"B": "#C9D8E5"}, pixel=0.075
        ).move_to(LEFT * 0.72 + UP * 0.95)
        lens = Circle(radius=0.38, color=TEAL, stroke_width=6).move_to(RIGHT * 0.78 + UP * 0.95)
        rays = VGroup(*[
            Line([x, 1.9, 0], [0.35, 0.95, 0], color=SAND, stroke_width=3)
            for x in [-1.55, -1.1, -0.65]
        ])
        focus = VGroup(
            Circle(radius=0.12, color=SAND, fill_color=SAND, fill_opacity=1)
                .move_to(RIGHT * 1.55 + UP * 0.95),
            Line(RIGHT * 1.25 + UP * 0.95, RIGHT * 1.85 + UP * 0.95,
                 color=WHITE, stroke_width=3),
            Line(RIGHT * 1.55 + UP * 0.65, RIGHT * 1.55 + UP * 1.25,
                 color=WHITE, stroke_width=3)
        )
        label = fit_line("WFPC2 + COSTAR • LIGHT IN FOCUS", 18, SAND, BOLD, 4.0)
        label.move_to(DOWN * 1.35)
        scene.play(FadeIn(telescope), FadeIn(lens), run_time=0.75)
        scene.play(Create(rays), run_time=0.85)
        scene.play(FadeIn(focus), Indicate(lens, color=TEAL), run_time=0.75)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(telescope), FadeOut(lens), FadeOut(rays),
                   FadeOut(focus), FadeOut(label), run_time=0.45)

    scene.play(FadeOut(caption), FadeOut(stars), run_time=0.3)




def sky_blue_pixel_story(scene, index, step):
    """Original animated science diagrams for Rayleigh scattering."""
    heading = fit_line(step["heading"], 24, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 20, WHITE, max_width=3.95)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.16).move_to(DOWN * 2.62)
    scene.play(FadeIn(caption, shift=UP * 0.12), run_time=0.45)

    if index == 1:
        sun = Circle(radius=0.48, color=SAND, fill_color=SAND, fill_opacity=1)
        sun.move_to(LEFT * 1.35 + UP * 1.2)
        rays = VGroup(*[
            Line(sun.get_center() + 0.62 * np.array([np.cos(a), np.sin(a), 0]),
                 sun.get_center() + 0.82 * np.array([np.cos(a), np.sin(a), 0]),
                 color=SAND, stroke_width=4)
            for a in np.linspace(0, TAU, 12, endpoint=False)
        ])
        white_beam = Line(LEFT * 0.75 + UP * 1.2, RIGHT * 1.65 + UP * 1.2,
                          color=WHITE, stroke_width=9)
        colours = ["#FF5B55", "#FF9D45", "#FFE16B", "#65D98A",
                   "#58B9FF", "#7188FF", "#B68CFF"]
        spectrum = VGroup(*[
            Line(LEFT * 0.25 + UP * (0.65 - i * 0.13),
                 RIGHT * 1.5 + UP * (0.65 - i * 0.13),
                 color=colour, stroke_width=5)
            for i, colour in enumerate(colours)
        ])
        label = fit_line("WHITE SUNLIGHT = MANY COLOURS", 19, TEAL, BOLD, 4.0)
        label.move_to(DOWN * 0.25)
        scene.play(FadeIn(sun), Create(rays), run_time=0.6)
        scene.play(Create(white_beam), run_time=0.6)
        scene.play(Transform(white_beam, spectrum), FadeIn(label), run_time=1.0)
        scene.play(FadeOut(sun), FadeOut(rays), FadeOut(white_beam), FadeOut(label), run_time=0.4)

    elif index == 2:
        points = [(-1.0, 1.15), (-0.45, 0.65), (0.1, 1.35),
                  (0.72, 0.8), (1.25, 1.25), (-0.8, 0.05), (0.35, 0.05)]
        molecules = VGroup(*[
            Circle(radius=0.105, color=TEAL, fill_color=TEAL, fill_opacity=1)
            .move_to([x, y, 0]) for x, y in points
        ])
        incoming = Line(LEFT * 1.9 + UP * 0.45, LEFT * 0.1 + UP * 0.45,
                        color="#7188FF", stroke_width=5)
        blue_scatter = VGroup(*[
            Arrow(LEFT * 0.1 + UP * 0.45, end, color="#58B9FF",
                  buff=0.05, stroke_width=4)
            for end in [UP * 1.95, RIGHT * 1.0 + UP * 1.65,
                        RIGHT * 1.2 + DOWN * 0.35, LEFT * 0.95 + DOWN * 0.55]
        ])
        red_ray = Line(LEFT * 0.1 + UP * 0.45, RIGHT * 1.9 + UP * 0.45,
                       color="#FF5B55", stroke_width=4)
        blue_label = fit_line("BLUE / VIOLET: SCATTERED MORE", 18, "#58B9FF", BOLD, 4.0)
        blue_label.move_to(DOWN * 0.95)
        red_label = fit_line("RED: PASSES THROUGH MORE", 18, "#FF8A72", BOLD, 4.0)
        red_label.move_to(DOWN * 1.4)
        scene.play(FadeIn(molecules), Create(incoming), run_time=0.6)
        scene.play(Create(blue_scatter), Create(red_ray), run_time=0.9)
        scene.play(FadeIn(blue_label), FadeIn(red_label), run_time=0.4)
        scene.play(FadeOut(molecules), FadeOut(incoming), FadeOut(blue_scatter),
                   FadeOut(red_ray), FadeOut(blue_label), FadeOut(red_label), run_time=0.4)

    elif index == 3:
        molecules = VGroup(*[
            Dot([x, y, 0], radius=0.095, color=TEAL)
            for x, y in [(-1.1, 0.9), (-0.45, 1.25), (0.3, 0.9), (0.9, 1.3)]
        ])
        eye = Ellipse(width=0.95, height=0.52, color=WHITE, stroke_width=4)
        eye.move_to(RIGHT * 1.2 + DOWN * 0.15)
        pupil = Circle(radius=0.16, color="#58B9FF", fill_color="#58B9FF",
                       fill_opacity=1).move_to(eye.get_center())
        rays = VGroup(*[
            Arrow(start, eye.get_left(), color="#58B9FF", buff=0.1, stroke_width=3)
            for start in [LEFT * 1.45 + UP * 1.1, LEFT * 0.95 + UP * 0.25,
                          LEFT * 1.25 + DOWN * 0.65]
        ])
        note = fit_line("OUR EYES RESPOND MORE TO BLUE THAN VIOLET",
                        17, SAND, BOLD, 4.0).move_to(DOWN * 1.1)
        scene.play(FadeIn(molecules), Create(rays), run_time=0.7)
        scene.play(FadeIn(eye), FadeIn(pupil), run_time=0.5)
        scene.play(FadeIn(note), run_time=0.4)
        scene.play(FadeOut(molecules), FadeOut(rays), FadeOut(eye),
                   FadeOut(pupil), FadeOut(note), run_time=0.4)

    else:
        sun = Circle(radius=0.38, color="#FF9D45", fill_color="#FF9D45",
                     fill_opacity=1).move_to(LEFT * 1.45 + UP * 1.15)
        horizon = Line(LEFT * 2.0 + DOWN * 0.65, RIGHT * 2.0 + DOWN * 0.65,
                       color=TEAL, stroke_width=4)
        path = VGroup(*[
            Line(LEFT * 1.1 + UP * 1.1, RIGHT * 1.35 + DOWN * 0.4,
                 color=colour, stroke_width=4)
            for colour in ["#FF9D45", "#FF5B55"]
        ])
        blue_dots = VGroup(*[
            Dot([x, y, 0], radius=0.07, color="#58B9FF")
            for x, y in [(-0.45, 0.65), (0.15, 0.38), (0.75, 0.1)]
        ])
        label = fit_line("LONGER AIR PATH = REDDER SUNSET",
                         18, SAND, BOLD, 4.0).move_to(DOWN * 1.25)
        scene.play(FadeIn(sun), Create(horizon), run_time=0.6)
        scene.play(Create(path), FadeIn(blue_dots), run_time=0.8)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(sun), FadeOut(horizon), FadeOut(path),
                   FadeOut(blue_dots), FadeOut(label), run_time=0.4)

    scene.wait(1.0)
    scene.play(FadeOut(caption), run_time=0.35)




def black_hole_pixel_story(scene, index, step):
    """Original pixel-art scenes for the first Event Horizon Telescope image."""
    heading = fit_line(step["heading"], 24, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 27, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.18).move_to(DOWN * 2.65)
    scene.play(FadeIn(caption, shift=UP * 0.12), run_time=0.45)

    if index == 1:
        earth_center = LEFT * 0.55 + UP * 0.55
        earth = Circle(radius=0.66, color="#4A9AC2",
                       fill_color="#164A70", fill_opacity=1).move_to(earth_center)
        land = pixel_sprite(
            ["...GG...", ".GGGGG..", "GG..GGG.", ".GGGG...", "...G...."],
            {"G": "#62B889"}, pixel=0.09
        ).move_to(earth_center)
        stations = VGroup()
        links = VGroup()
        for angle in np.linspace(0, TAU, 8, endpoint=False):
            position = earth_center + np.array([
                1.12 * math.cos(angle), 1.12 * math.sin(angle), 0
            ])
            dish = pixel_sprite(
                ["..W..", ".WWW.", "..B..", ".B.B."],
                {"W": MINT, "B": TEAL}, pixel=0.045
            ).move_to(position)
            stations.add(dish)
            links.add(Line(position, earth_center, color=TEAL, stroke_width=1.4))
        label = fit_line("8 RADIO OBSERVATORIES • ONE VIRTUAL TELESCOPE",
                         17, SAND, BOLD, 4.0).move_to(DOWN * 1.3)
        scene.play(FadeIn(earth), FadeIn(land), Create(links), run_time=0.8)
        scene.play(LaggedStart(*[FadeIn(station) for station in stations],
                               lag_ratio=0.08), run_time=0.9)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(earth), FadeOut(land), FadeOut(links),
                   FadeOut(stations), FadeOut(label), run_time=0.4)

    elif index == 2:
        drive = pixel_sprite(
            ["BBBBBBBB", "BWWWWWWB", "BWWWWWWB", "BBBBBBBB"],
            {"B": "#91AFC2", "W": "#244A65"}, pixel=0.105
        ).move_to(LEFT * 1.25 + UP * 0.55)
        computer = pixel_sprite(
            ["BBBBBBBBBB", "BWWWWWWWWB", "BWWWWWWWWB",
             "BWWWWWWWWB", "BBBBBBBBBB", "..BBBB.."],
            {"B": "#2F9E92", "W": "#B7D6E3"}, pixel=0.085
        ).move_to(RIGHT * 1.25 + UP * 0.55)
        transfer = Arrow(LEFT * 0.55 + UP * 0.55,
                         RIGHT * 0.55 + UP * 0.55,
                         color=SAND, buff=0.08, stroke_width=4)
        label = fit_line("≈350 TERABYTES / DAY / EACH TELESCOPE",
                         17, SAND, BOLD, 4.0).move_to(DOWN * 1.25)
        scene.play(FadeIn(drive), FadeIn(computer), Create(transfer), run_time=0.8)
        scene.play(drive.animate.shift(RIGHT * 1.45), run_time=1.0, rate_func=smooth)
        scene.play(FadeIn(label), run_time=0.4)
        scene.play(FadeOut(drive), FadeOut(computer), FadeOut(transfer),
                   FadeOut(label), run_time=0.4)

    elif index == 3:
        centre = UP * 0.55
        glow = Circle(radius=1.0, color="#FFD58C", stroke_width=4).move_to(centre)
        ring = Circle(radius=0.78, color="#FF9D52", stroke_width=24).move_to(centre)
        shadow = Circle(radius=0.47, color="#020611",
                        fill_color="#020611", fill_opacity=1).move_to(centre)
        gas = VGroup(*[
            Dot(centre + np.array([0.88 * np.cos(a), 0.88 * np.sin(a), 0]),
                radius=0.07, color="#FFE0A5")
            for a in np.linspace(0, TAU, 8, endpoint=False)
        ])
        distance = fit_line("M87* • ABOUT 55 MILLION LIGHT-YEARS AWAY",
                            17, TEAL, BOLD, 4.0).move_to(UP * 1.75)
        meaning = fit_line("A DARK SHADOW • GLOWING GAS AROUND IT",
                           17, SAND, BOLD, 4.0).move_to(DOWN * 1.25)
        scene.play(Create(glow), Create(ring), FadeIn(shadow), run_time=0.9)
        scene.play(LaggedStart(*[FadeIn(dot) for dot in gas],
                               lag_ratio=0.08), run_time=0.7)
        scene.play(FadeIn(distance), FadeIn(meaning), run_time=0.4)
        scene.play(FadeOut(glow), FadeOut(ring), FadeOut(shadow),
                   FadeOut(gas), FadeOut(distance), FadeOut(meaning), run_time=0.4)

    scene.play(FadeOut(caption), run_time=0.35)


def voyager_probe_sprite(pixel=0.075):
    """Original pixel-art Voyager probe for the Golden Record story."""
    core = pixel_sprite(
        ["...S...", "..SSS..", ".SSSSS.", "..S.S..", "..S.S..", "...S..."],
        {"S": "#DCE8EF"}, pixel=pixel
    )
    left_panel = pixel_sprite(
        ["PPPP", "P..P", "PPPP"],
        {"P": "#2F9E92"}, pixel=pixel
    ).move_to(LEFT * 0.58)
    right_panel = pixel_sprite(
        ["PPPP", "P..P", "PPPP"],
        {"P": "#2F9E92"}, pixel=pixel
    ).move_to(RIGHT * 0.58)
    antenna_stem = Line(UP * 0.25, UP * 0.55, color=MINT, stroke_width=2)
    antenna = Circle(radius=pixel * 1.9, color=SAND, stroke_width=2).move_to(UP * 0.62)
    return VGroup(core, left_panel, right_panel, antenna_stem, antenna)


def voyager_record_sprite(radius=0.58):
    """Original illustration of the gold-plated phonograph record."""
    disc = Circle(
        radius=radius, color="#FFE7A8", stroke_width=3,
        fill_color="#C99532", fill_opacity=1
    )
    grooves = VGroup(*[
        Circle(radius=radius * scale, color="#F7D77E", stroke_width=1.1)
        for scale in (0.82, 0.64, 0.46, 0.28)
    ])
    centre = Circle(
        radius=radius * 0.10, color="#8A5A22",
        fill_color="#8A5A22", fill_opacity=1
    )
    return VGroup(disc, grooves, centre)


def voyager_pixel_story(scene, index, step):
    """Original pixel-art scenes for the Voyager Golden Record story."""
    heading = fit_line(step["heading"], 24, SAND, BOLD, max_width=4.0)
    body = fit_paragraph(step["body"], 27, WHITE, max_width=4.0)
    caption = VGroup(heading, body).arrange(DOWN, buff=0.18).move_to(DOWN * 2.65)
    scene.play(FadeIn(caption, shift=UP * 0.12), run_time=0.45)

    if index == 1:
        earth_center = LEFT * 0.88 + UP * 0.55
        earth = Circle(
            radius=0.62, color="#4A9AC2",
            fill_color="#164A70", fill_opacity=1
        ).move_to(earth_center)
        land = pixel_sprite(
            ["...GG...", ".GGGGG..", "GG..GGG.", ".GGGG...", "...G...."],
            {"G": "#62B889"}, pixel=0.075
        ).move_to(earth_center)
        voyager_two = voyager_probe_sprite(0.07).move_to(RIGHT * 0.92 + UP * 0.88)
        voyager_one = voyager_probe_sprite(0.07).move_to(RIGHT * 0.92 + DOWN * 0.18)
        trail_two = DashedLine(
            earth_center + RIGHT * 0.48 + UP * 0.2,
            RIGHT * 0.55 + UP * 0.88, color=TEAL, stroke_width=2
        )
        trail_one = DashedLine(
            earth_center + RIGHT * 0.48 + DOWN * 0.15,
            RIGHT * 0.55 + DOWN * 0.18, color=TEAL, stroke_width=2
        )
        date_two = fit_line("VOYAGER 2 • 20 AUG 1977", 17, SAND, BOLD, 4.0).move_to(DOWN * 1.18)
        date_one = fit_line("VOYAGER 1 • 5 SEP 1977", 17, MINT, BOLD, 4.0).move_to(DOWN * 1.62)
        scene.play(FadeIn(earth), FadeIn(land), Create(trail_two), Create(trail_one), run_time=0.7)
        scene.play(FadeIn(voyager_two), FadeIn(voyager_one), run_time=0.6)
        scene.play(
            voyager_two.animate.shift(RIGHT * 0.32 + UP * 0.12),
            voyager_one.animate.shift(RIGHT * 0.32 + DOWN * 0.12),
            run_time=1.0, rate_func=smooth
        )
        scene.play(FadeIn(date_two), FadeIn(date_one), run_time=0.35)
        scene.play(
            FadeOut(earth), FadeOut(land), FadeOut(voyager_two), FadeOut(voyager_one),
            FadeOut(trail_two), FadeOut(trail_one), FadeOut(date_two), FadeOut(date_one),
            run_time=0.4
        )

    elif index == 2:
        record = voyager_record_sprite(0.72).move_to(UP * 0.55)
        picture = Rectangle(width=0.62, height=0.52, color=TEAL, stroke_width=4).move_to(LEFT * 1.32 + UP * 0.55)
        picture_sun = Circle(radius=0.09, color=SAND, fill_color=SAND, fill_opacity=1).move_to(LEFT * 1.45 + UP * 0.68)
        picture_hill = VGroup(
            Line(LEFT * 1.58 + UP * 0.35, LEFT * 1.32 + UP * 0.58, color=MINT, stroke_width=3),
            Line(LEFT * 1.32 + UP * 0.58, LEFT * 1.06 + UP * 0.35, color=MINT, stroke_width=3)
        )
        sound_waves = VGroup(*[
            Line(
                RIGHT * (0.95 + offset) + UP * (0.25 + height),
                RIGHT * (0.95 + offset) + UP * (0.75 - height),
                color=TEAL, stroke_width=4
            )
            for offset, height in ((0.0, 0.16), (0.18, 0.02), (0.36, 0.20), (0.54, 0.08))
        ])
        music_note = Text("♪", font_size=64, color=SAND).move_to(RIGHT * 1.34 + DOWN * 0.28)
        contents = fit_line("IMAGES • EARTH SOUNDS • MUSIC", 16, SAND, BOLD, 4.0).move_to(DOWN * 1.32)
        languages = fit_line("GREETINGS IN 55 LANGUAGES", 17, MINT, BOLD, 4.0).move_to(DOWN * 1.72)
        scene.play(FadeIn(record), Create(picture), FadeIn(picture_sun), Create(picture_hill), run_time=0.8)
        scene.play(Create(sound_waves), FadeIn(music_note), run_time=0.7)
        scene.play(FadeIn(contents), FadeIn(languages), run_time=0.4)
        scene.play(
            FadeOut(record), FadeOut(picture), FadeOut(picture_sun), FadeOut(picture_hill),
            FadeOut(sound_waves), FadeOut(music_note), FadeOut(contents), FadeOut(languages),
            run_time=0.4
        )

    elif index == 3:
        cover = RoundedRectangle(
            width=1.55, height=1.55, corner_radius=0.08,
            color="#C8D4DC", stroke_width=3, fill_color="#AAB9C4", fill_opacity=1
        ).move_to(LEFT * 0.78 + UP * 0.55)
        engraved = VGroup(
            Line(LEFT * 1.25 + UP * 0.92, LEFT * 0.30 + UP * 0.92, color=NAVY, stroke_width=2),
            Line(LEFT * 1.25 + UP * 0.72, LEFT * 0.30 + UP * 0.72, color=NAVY, stroke_width=2),
            Circle(radius=0.16, color=NAVY, stroke_width=2).move_to(LEFT * 0.78 + UP * 0.38),
            Line(LEFT * 1.08 + UP * 0.12, LEFT * 0.48 + UP * 0.12, color=NAVY, stroke_width=2)
        )
        arrow = Arrow(LEFT * 0.02 + UP * 0.55, RIGHT * 0.02 + UP * 0.55, color=SAND, buff=0.05, stroke_width=4)
        record = voyager_record_sprite(0.66).move_to(RIGHT * 0.88 + UP * 0.55)
        labels = VGroup(
            fit_line("HOW TO PLAY", 17, MINT, BOLD, 1.8).move_to(LEFT * 0.78 + DOWN * 0.62),
            fit_line("WHERE EARTH IS", 17, SAND, BOLD, 1.9).move_to(RIGHT * 0.88 + DOWN * 0.62)
        )
        time_label = fit_line("A TIME CAPSULE, NOT A BROADCAST", 17, TEAL, BOLD, 4.0).move_to(DOWN * 1.35)
        scene.play(FadeIn(cover), Create(engraved), FadeIn(record), run_time=0.8)
        scene.play(Create(arrow), FadeIn(labels), FadeIn(time_label), run_time=0.6)
        scene.play(record.animate.scale(1.08), run_time=0.6, rate_func=smooth)
        scene.play(
            FadeOut(cover), FadeOut(engraved), FadeOut(arrow), FadeOut(record),
            FadeOut(labels), FadeOut(time_label), run_time=0.4
        )

    scene.play(FadeOut(caption), run_time=0.35)


def atom_to_galaxy_scale_story(scene, index, step):
    """Original animated scale comparisons for atom-to-observable-universe lesson."""
    stars = VGroup(*[
        Dot([((i * 31) % 43) / 10 - 2.1, ((i * 17) % 67) / 10 - 3.1, 0],
            radius=0.012, color=PALE)
        for i in range(42)
    ])
    heading = fit_line(step["heading"], 23, SAND, BOLD, max_width=4.05)
    heading.move_to(UP * 2.15)
    scene.add(stars)
    scene.play(FadeIn(heading, shift=UP * 0.12), run_time=0.55)

    if index == 1:
        atom_center = LEFT * 1.08 + UP * 0.25
        cell_center = RIGHT * 1.05 + UP * 0.25
        cloud = Circle(radius=0.58, color="#55BDE8", stroke_width=3,
                       fill_color="#55BDE8", fill_opacity=0.08).move_to(atom_center)
        shell = Circle(radius=0.40, color=TEAL, stroke_width=2).move_to(atom_center)
        nucleus = Dot(atom_center, radius=0.12, color=SAND)
        electrons = VGroup(*[
            Dot(atom_center + np.array([0.40*np.cos(a), 0.40*np.sin(a), 0]),
                radius=0.055, color=WHITE)
            for a in [0.3, 2.45, 4.55]
        ])
        atom = VGroup(cloud, shell, nucleus, electrons)
        membrane = Circle(radius=0.68, color="#76D6C7", stroke_width=5,
                          fill_color="#1D6B76", fill_opacity=0.20).move_to(cell_center)
        cell_nucleus = Circle(radius=0.18, color=SAND, stroke_width=3,
                              fill_color="#C77B55", fill_opacity=0.85).move_to(cell_center + LEFT*0.12)
        organelles = VGroup(*[
            Dot(cell_center + np.array([x, y, 0]), radius=0.055, color=c)
            for x, y, c in [(-0.35, 0.28, TEAL), (0.32, 0.32, SAND),
                            (0.35, -0.28, "#55BDE8"), (-0.32, -0.32, WHITE)]
        ])
        cell = VGroup(membrane, cell_nucleus, organelles)
        atom_label = fit_line("ATOM • ~10⁻¹⁰ m", 17, TEAL, BOLD, 1.9)
        atom_label.move_to(atom_center + UP*0.93)
        cell_label = fit_line("ANIMAL CELL • ~10 μm", 16, TEAL, BOLD, 2.05)
        cell_label.move_to(cell_center + UP*1.0)
        connector = Arrow(LEFT*0.24 + UP*0.15, RIGHT*0.22 + UP*0.15,
                          color=SAND, buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.22)
        ratio = fit_line("ABOUT 100,000× WIDER", 22, SAND, BOLD, 3.9)
        ratio.move_to(DOWN*0.95)
        scene.play(FadeIn(atom), FadeIn(cell), FadeIn(atom_label), FadeIn(cell_label),
                   run_time=0.85)
        scene.play(Create(connector), FadeIn(ratio), run_time=0.65)
        scene.play(Indicate(cell, color=TEAL, scale_factor=1.06), run_time=0.65)
        scene.play(FadeOut(atom), FadeOut(cell), FadeOut(atom_label), FadeOut(cell_label),
                   FadeOut(connector), FadeOut(ratio), run_time=0.4)

    elif index == 2:
        person_x = -1.48
        person = VGroup(
            Circle(radius=0.12, color=WHITE, fill_color=WHITE, fill_opacity=1).move_to([person_x, 0.63, 0]),
            Line([person_x, 0.48, 0], [person_x, -0.15, 0], color=WHITE, stroke_width=6),
            Line([person_x, 0.25, 0], [person_x-0.24, -0.02, 0], color=WHITE, stroke_width=5),
            Line([person_x, 0.25, 0], [person_x+0.25, -0.02, 0], color=WHITE, stroke_width=5),
            Line([person_x, -0.15, 0], [person_x-0.2, -0.55, 0], color=WHITE, stroke_width=5),
            Line([person_x, -0.15, 0], [person_x+0.22, -0.55, 0], color=WHITE, stroke_width=5),
        )
        earth_center = LEFT*0.05 + UP*0.28
        earth = Circle(radius=0.46, color="#55BDE8", stroke_width=4,
                       fill_color="#17659A", fill_opacity=1).move_to(earth_center)
        land = VGroup(
            Ellipse(width=0.30, height=0.16, color="#65C78C",
                    fill_color="#65C78C", fill_opacity=1).rotate(0.4).move_to(earth_center + LEFT*0.10 + UP*0.12),
            Ellipse(width=0.18, height=0.28, color="#65C78C",
                    fill_color="#65C78C", fill_opacity=1).rotate(-0.5).move_to(earth_center + RIGHT*0.16 + DOWN*0.08),
        )
        sun_center = RIGHT*1.28 + UP*0.28
        sun_glow = Circle(radius=0.94, color="#E88D42", stroke_width=2,
                          fill_color="#E88D42", fill_opacity=0.10).move_to(sun_center)
        sun = Circle(radius=0.68, color="#FFCF70", stroke_width=3,
                     fill_color="#F59C43", fill_opacity=1).move_to(sun_center)
        rays = VGroup(*[
            Line(sun_center + np.array([0.79*np.cos(a),0.79*np.sin(a),0]),
                 sun_center + np.array([0.93*np.cos(a),0.93*np.sin(a),0]),
                 color="#FFD27A", stroke_width=4)
            for a in np.linspace(0, TAU, 12, endpoint=False)
        ])
        person_label = fit_line("YOU", 17, WHITE, BOLD).move_to([person_x, 1.1, 0])
        earth_label = fit_line("EARTH", 17, "#7DD3FC", BOLD).move_to(earth_center + UP*0.78)
        sun_label = fit_line("SUN", 17, SAND, BOLD).move_to(sun_center + UP*1.0)
        ratio = fit_line("SUN ≈ 109 EARTH DIAMETERS", 22, SAND, BOLD, 4.0)
        ratio.move_to(DOWN*1.10)
        scene.play(FadeIn(person), FadeIn(earth), FadeIn(land), FadeIn(sun_glow),
                   FadeIn(sun), Create(rays), FadeIn(person_label), FadeIn(earth_label),
                   FadeIn(sun_label), run_time=0.95)
        scene.play(Indicate(sun, color=SAND, scale_factor=1.04), FadeIn(ratio),
                   run_time=0.85)
        scene.play(FadeOut(person), FadeOut(earth), FadeOut(land), FadeOut(sun_glow),
                   FadeOut(sun), FadeOut(rays), FadeOut(person_label),
                   FadeOut(earth_label), FadeOut(sun_label), FadeOut(ratio), run_time=0.4)

    else:
        galaxy_center = LEFT*0.95 + UP*0.18
        core = Circle(radius=0.20, color="#FFE0A0",
                      fill_color="#FFE0A0", fill_opacity=0.95).move_to(galaxy_center)
        arms = VGroup()
        for arm in range(3):
            dots = VGroup()
            offset = arm * TAU / 3
            for j in range(34):
                t = j / 33
                angle = offset + t * 2.7 * PI
                radius = 0.18 + 0.78 * t
                point = galaxy_center + np.array([radius*np.cos(angle), radius*0.53*np.sin(angle), 0])
                dots.add(Dot(point, radius=0.018 + 0.012*(1-t),
                             color=["#8BE2D2", "#9AC8FF", "#FFD27A"][arm]))
            arms.add(dots)
        galaxy_ring = Ellipse(width=2.05, height=1.10, color="#89B8D8",
                              stroke_width=2, fill_opacity=0).move_to(galaxy_center)
        universe_center = RIGHT*1.12 + UP*0.18
        universe = Circle(radius=0.95, color="#9CC9E8", stroke_width=3,
                          fill_color="#173A62", fill_opacity=0.18).move_to(universe_center)
        universe_stars = VGroup(*[
            Dot(universe_center + np.array([0.78*np.cos(a), 0.78*np.sin(a), 0]),
                radius=0.027, color=[TEAL, WHITE, SAND][i % 3])
            for i, a in enumerate(np.linspace(0, TAU, 14, endpoint=False))
        ])
        universe_core = Circle(radius=0.20, color="#FFE0A0", fill_color="#FFE0A0",
                               fill_opacity=0.85).move_to(universe_center)
        galaxy_label = fit_line("MILKY WAY", 17, TEAL, BOLD).move_to(galaxy_center + UP*0.92)
        universe_label = fit_line("OBSERVABLE UNIVERSE", 16, "#9CC9E8", BOLD, 2.2)
        universe_label.move_to(universe_center + UP*1.12)
        size_a = fit_line("~100,000 LIGHT-YEARS", 15, WHITE, BOLD, 2.1)
        size_a.move_to(galaxy_center + DOWN*0.82)
        size_b = fit_line("~92 BILLION LIGHT-YEARS", 15, WHITE, BOLD, 2.15)
        size_b.move_to(universe_center + DOWN*1.12)
        ratio = fit_line("≈37 POWERS OF TEN", 25, SAND, BOLD, 3.7)
        ratio.move_to(DOWN*1.85)
        scene.play(FadeIn(core), LaggedStart(*[FadeIn(a) for a in arms], lag_ratio=0.08),
                   Create(galaxy_ring), FadeIn(galaxy_label), FadeIn(size_a), run_time=1.0)
        scene.play(FadeIn(universe), FadeIn(universe_stars), FadeIn(universe_core),
                   FadeIn(universe_label), FadeIn(size_b), run_time=0.95)
        scene.play(Indicate(universe, color="#9CC9E8", scale_factor=1.03),
                   FadeIn(ratio), run_time=0.8)
        scene.play(FadeOut(core), FadeOut(arms), FadeOut(galaxy_ring), FadeOut(galaxy_label),
                   FadeOut(size_a), FadeOut(universe), FadeOut(universe_stars),
                   FadeOut(universe_core), FadeOut(universe_label), FadeOut(size_b),
                   FadeOut(ratio), run_time=0.45)

    scene.play(FadeOut(heading), FadeOut(stars), run_time=0.35)




def modern_topic_visual(scene, lesson_id, index):
    """Original animated visual motifs for five new Shorts."""
    if lesson_id == "gps-satellite-navigation":
        earth = Circle(radius=0.9, color="#3D8BC9", fill_color="#174A78", fill_opacity=1)
        earth.move_to(DOWN * 0.25)
        sats = VGroup()
        beams = VGroup()
        for pos in [LEFT*1.35+UP*1.7, RIGHT*1.35+UP*1.7, LEFT*1.8+DOWN*0.15, RIGHT*1.8+DOWN*0.15]:
            sat = VGroup(Rectangle(width=0.28,height=0.18,color=SAND,fill_opacity=1), Line(LEFT*0.42,RIGHT*0.42,color=TEAL,stroke_width=4)).move_to(pos)
            sats.add(sat)
            beams.add(DashedLine(pos, earth.get_center(), color=TEAL, dash_length=0.09, stroke_width=2))
        scene.play(FadeIn(earth), LaggedStart(*[FadeIn(x) for x in sats],lag_ratio=0.12), run_time=0.7)
        scene.play(*[Create(x) for x in beams], run_time=0.7)
        scene.play(*[Indicate(x,color=SAND) for x in sats], run_time=0.45)
        scene.play(FadeOut(VGroup(earth,sats,beams)), run_time=0.3)
    elif lesson_id == "bioluminescence-ocean":
        waves=VGroup(*[Arc(radius=1.0+0.28*j,start_angle=PI,angle=PI,color="#1BC8D5",stroke_width=5).shift(DOWN*0.55+UP*0.17*j) for j in range(3)])
        plankton=VGroup(*[Dot([((i*17)%31)/10-1.5,((i*11)%19)/10-0.7,0],radius=0.035,color="#72F5FF") for i in range(38)])
        scene.play(LaggedStart(*[Create(w) for w in waves],lag_ratio=0.15),run_time=0.75)
        scene.play(LaggedStart(*[FadeIn(p,scale=1.8) for p in plankton],lag_ratio=0.025),run_time=0.7)
        scene.play(*[Indicate(plankton[i],color=WHITE) for i in range(0,38,4)],run_time=0.6)
        scene.play(FadeOut(VGroup(waves,plankton)),run_time=0.3)
    elif lesson_id == "roman-concrete":
        wall=VGroup()
        for row in range(4):
            for col in range(4):
                brick=Rectangle(width=0.72,height=0.36,color="#D5A96C",fill_color="#A87948",fill_opacity=1,stroke_width=2)
                brick.move_to([(-1.1+col*0.73)+(0.35 if row%2 else 0),-0.55+row*0.38,0])
                wall.add(brick)
        crystals=VGroup(*[Line([0,0,0],[0.12,0.35,0],color="#8DE4E1",stroke_width=4).move_to([(-0.8+(i%3)*0.8),-0.2+(i//3)*0.3,0]) for i in range(9)])
        scene.play(LaggedStart(*[FadeIn(b,shift=UP*0.08) for b in wall],lag_ratio=0.04),run_time=0.8)
        scene.play(LaggedStart(*[GrowFromCenter(c) for c in crystals],lag_ratio=0.08),run_time=0.65)
        scene.play(*[Indicate(crystals[i],color=WHITE) for i in [0,4,8]],run_time=0.5)
        scene.play(FadeOut(VGroup(wall,crystals)),run_time=0.3)
    elif lesson_id == "moon-phases":
        earth=Circle(radius=0.28,color="#4E9FE0",fill_color="#2675B8",fill_opacity=1)
        orbit=Circle(radius=1.45,color="#7890A5",stroke_opacity=0.65)
        moons=VGroup()
        for angle in [0,PI/2,PI,3*PI/2]:
            m=Circle(radius=0.25,color="#E8E4D8",fill_color="#E8E4D8",fill_opacity=1).move_to([1.45*np.cos(angle),1.45*np.sin(angle),0])
            shadow=Circle(radius=0.25,color="#4A5260",fill_color="#4A5260",fill_opacity=1).move_to(m.get_center()+LEFT*0.12)
            moons.add(VGroup(m,shadow))
        sun=Circle(radius=0.22,color=SAND,fill_color=SAND,fill_opacity=1).move_to(LEFT*2.0)
        scene.play(FadeIn(sun),Create(orbit),FadeIn(earth),run_time=0.65)
        scene.play(LaggedStart(*[FadeIn(m,scale=0.7) for m in moons],lag_ratio=0.18),run_time=0.8)
        scene.play(Rotate(moons,angle=PI/3,about_point=earth.get_center()),run_time=0.8)
        scene.play(FadeOut(VGroup(sun,orbit,earth,moons)),run_time=0.3)
    elif lesson_id == "deep-ocean-pressure":
        layers=VGroup(*[Rectangle(width=4.0,height=0.72,fill_color=["#2586A8","#14617F","#0C3F60","#082943"][i],fill_opacity=1,stroke_width=0).move_to(DOWN*0.35-DOWN*0.72*i) for i in range(4)])
        sub=VGroup(Circle(radius=0.25,color=SAND,fill_color="#D6A94F",fill_opacity=1),Rectangle(width=0.75,height=0.22,color=SAND,fill_color="#D6A94F",fill_opacity=1)).move_to(UP*1.2)
        gauge=Circle(radius=0.42,color=WHITE).move_to(RIGHT*1.45+DOWN*0.2)
        needle=Line(gauge.get_center(),gauge.get_center()+UP*0.28,color="#FF8C69",stroke_width=4)
        scene.play(LaggedStart(*[FadeIn(x) for x in layers],lag_ratio=0.12),FadeIn(sub),run_time=0.8)
        scene.play(sub.animate.shift(DOWN*1.5),Create(gauge),GrowFromCenter(needle),run_time=0.9)
        scene.play(Rotate(needle,angle=-PI/2,about_point=gauge.get_center()),Indicate(sub,color=SAND),run_time=0.65)
        scene.play(FadeOut(VGroup(layers,sub,gauge,needle)),run_time=0.3)

    elif lesson_id == "neptune-math-discovery":
        if index == 1:
            orbit = Ellipse(width=3.5, height=1.55, color="#6B879D", stroke_width=2).move_to(UP*0.35)
            sun = Circle(radius=0.24, color=SAND, fill_color=SAND, fill_opacity=1).move_to(LEFT*1.2+UP*0.35)
            uranus = Circle(radius=0.25, color="#79C8D8", fill_color="#367F9B", fill_opacity=1).move_to(RIGHT*0.65+UP*1.05)
            unseen = Circle(radius=0.30, color="#4C83D1", fill_color="#183D78", fill_opacity=1).move_to(RIGHT*1.25+DOWN*0.55)
            tug = Arrow(unseen.get_left(), uranus.get_right(), color=SAND, buff=0.08, stroke_width=4)
            label = fit_line("AN UNSEEN PLANET'S GRAVITY", 19, TEAL, BOLD, 4.0).move_to(DOWN*1.45)
            scene.play(Create(orbit), FadeIn(sun), FadeIn(uranus), FadeIn(unseen), run_time=0.8)
            scene.play(GrowArrow(tug), Indicate(uranus, color=SAND), FadeIn(label), run_time=0.8)
            scene.play(FadeOut(VGroup(orbit, sun, uranus, unseen, tug, label)), run_time=0.35)
        elif index == 2:
            paper = RoundedRectangle(width=3.45, height=2.1, corner_radius=0.12,
                                     color="#D9E4E8", fill_color="#D9E4E8", fill_opacity=1).move_to(UP*0.45)
            lines = VGroup(
                Text("URANUS ORBIT DATA", font_size=20, color="#17334C", weight=BOLD),
                Text("NEWTON'S GRAVITY", font_size=22, color="#17334C", weight=BOLD),
                Text("PREDICTED SKY POSITION", font_size=18, color="#287F83", weight=BOLD),
            ).arrange(DOWN, buff=0.28).move_to(paper.get_center())
            pencil = Line(LEFT*1.45+DOWN*1.45, RIGHT*1.45+DOWN*1.45, color=SAND, stroke_width=6)
            target = Circle(radius=0.17, color="#4C83D1", fill_color="#4C83D1", fill_opacity=1).move_to(RIGHT*1.35+DOWN*1.45)
            scene.play(FadeIn(paper), LaggedStart(*[FadeIn(line, shift=UP*0.08) for line in lines], lag_ratio=0.18), run_time=0.9)
            scene.play(Create(pencil), FadeIn(target), Indicate(lines[2], color=TEAL), run_time=0.7)
            scene.play(FadeOut(VGroup(paper, lines, pencil, target)), run_time=0.35)
        else:
            stars = VGroup(*[
                Dot([((i*17)%35)/10-1.7, ((i*11)%25)/10-0.75, 0], radius=0.025, color=WHITE)
                for i in range(28)
            ])
            telescope = VGroup(
                Rectangle(width=1.0, height=0.28, color="#B7C9D8", fill_color="#45627A", fill_opacity=1),
                Circle(radius=0.18, color=SAND, fill_color="#D6B45C", fill_opacity=1).shift(RIGHT*0.55),
                Line(LEFT*0.15+DOWN*0.12, LEFT*0.45+DOWN*0.72, color=TEAL, stroke_width=4),
                Line(LEFT*0.15+DOWN*0.12, RIGHT*0.15+DOWN*0.68, color=TEAL, stroke_width=4),
            ).move_to(LEFT*1.0+UP*0.35)
            planet = Circle(radius=0.22, color="#76B9F4", fill_color="#2766A8", fill_opacity=1).move_to(RIGHT*1.15+UP*0.65)
            target = VGroup(
                Circle(radius=0.43, color=SAND, stroke_width=2).move_to(planet.get_center()),
                Line(planet.get_center()+LEFT*0.58, planet.get_center()+RIGHT*0.58, color=SAND, stroke_width=2),
                Line(planet.get_center()+UP*0.58, planet.get_center()+DOWN*0.58, color=SAND, stroke_width=2),
            )
            date = fit_line("23 SEPTEMBER 1846", 20, SAND, BOLD, 3.8).move_to(DOWN*1.35)
            scene.play(FadeIn(stars), FadeIn(telescope), run_time=0.75)
            scene.play(FadeIn(planet), Create(target), FadeIn(date), run_time=0.75)
            scene.play(Indicate(planet, color=WHITE), run_time=0.55)
            scene.play(FadeOut(VGroup(stars, telescope, planet, target, date)), run_time=0.35)



class AcademyLessonShort(Scene):
    def construct(self):
        lesson_path = os.environ.get("ACADEMY_LESSON_FILE", "creator-studio/lessons/active-lesson.json")
        lesson = json.loads(Path(lesson_path).read_text(encoding="utf-8"))
        self.camera.background_color = NAVY

        brand = fit_line("ADVENTURE OF EDUCATION", 20, TEAL, BOLD, 4.0)
        brand.to_edge(UP, buff=0.42)
        self.add(brand)

        is_apollo = lesson.get("title", "").startswith("Apollo 13:")
        is_hubble = lesson.get("title", "").startswith("Hubble's Blurry Vision:")
        is_black_hole = lesson.get("title", "").startswith("The First Black Hole Image:")
        is_voyager = lesson.get("title", "").startswith("Voyager's Golden Record:")
        is_neptune = lesson.get("id") == "neptune-math-discovery"
        is_scale = lesson.get("title", "").startswith("From an Atom to the Observable Universe:")
        if is_apollo:
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
        elif is_hubble:
            telescope = pixel_sprite(
                ["....BBBBBBBB....", "...BBBBBBBBBB...",
                 "BBBBBBBBBBBBBBBB", "...BBBBBBBBBB...",
                 "....BBBBBBBB...."],
                {"B": "#C9D8E5"}, pixel=0.085
            ).move_to(UP * 0.8)
            astronaut = pixel_sprite(
                ["..WWW..", ".WSSSW.", "WSSSSSW", ".WWWWW.",
                 "..W.W..", ".W...W."],
                {"W": WHITE, "S": SAND}, pixel=0.12
            ).move_to(LEFT * 1.15 + DOWN * 0.45)
            cold_open = fit_paragraph(
                "BLURRY SPACE IMAGES. A REPAIR CREW IN ORBIT.",
                30, SAND, max_width=4.0
            ).move_to(DOWN * 1.55)
            self.play(FadeIn(telescope), FadeIn(astronaut), run_time=0.65)
            self.play(astronaut.animate.shift(RIGHT * 0.25), FadeIn(cold_open),
                      run_time=0.85, rate_func=smooth)
            self.wait(1.3)
            self.play(FadeOut(telescope), FadeOut(astronaut), FadeOut(cold_open),
                      run_time=0.35)
        elif is_black_hole:
            earth_center = LEFT * 0.85 + UP * 0.55
            earth = Circle(radius=0.58, color="#4A9AC2",
                           fill_color="#164A70", fill_opacity=1).move_to(earth_center)
            land = pixel_sprite(
                ["...GG...", ".GGGGG..", "GG..GGG.", ".GGGG...", "...G...."],
                {"G": "#62B889"}, pixel=0.075
            ).move_to(earth_center)
            stations = VGroup()
            links = VGroup()
            for angle in np.linspace(0, TAU, 8, endpoint=False):
                position = earth_center + np.array([
                    0.98 * np.cos(angle), 0.98 * np.sin(angle), 0
                ])
                stations.add(pixel_sprite(
                    ["..W..", ".WWW.", "..B..", ".B.B."],
                    {"W": MINT, "B": TEAL}, pixel=0.04
                ).move_to(position))
                links.add(Line(position, earth_center, color=TEAL, stroke_width=1.2))
            ring_center = RIGHT * 1.05 + UP * 0.55
            ring = Circle(radius=0.52, color="#FF9D52", stroke_width=18).move_to(ring_center)
            shadow = Circle(radius=0.31, color="#020611",
                            fill_color="#020611", fill_opacity=1).move_to(ring_center)
            cold_open = fit_paragraph(
                "EIGHT TELESCOPES. ONE EARTH-SIZED EYE.",
                29, SAND, max_width=4.0
            ).move_to(DOWN * 1.45)
            self.play(FadeIn(earth), FadeIn(land), Create(links), run_time=0.65)
            self.play(LaggedStart(*[FadeIn(station) for station in stations],
                                  lag_ratio=0.07), run_time=0.8)
            self.play(Create(ring), FadeIn(shadow), FadeIn(cold_open), run_time=0.85)
            self.wait(1.1)
            self.play(FadeOut(earth), FadeOut(land), FadeOut(links),
                      FadeOut(stations), FadeOut(ring), FadeOut(shadow),
                      FadeOut(cold_open), run_time=0.4)


        elif is_scale:
            atom = Circle(radius=0.42, color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.12).move_to(LEFT*1.25 + UP*0.45)
            nucleus = Dot(atom.get_center(), radius=0.10, color=SAND)
            galaxy = VGroup(*[
                Dot([1.15 + 0.12*j*np.cos(j*0.35), 0.45 + 0.06*j*np.sin(j*0.35), 0],
                    radius=0.025, color=[TEAL, WHITE, SAND][j % 3])
                for j in range(1, 24)
            ])
            path = Arrow(LEFT*0.65 + UP*0.45, RIGHT*0.65 + UP*0.45,
                         color=SAND, buff=0.04, stroke_width=4)
            headline = fit_line("HOW BIG IS BIG?", 33, WHITE, BOLD, 3.8).move_to(DOWN*1.1)
            punch = fit_line("≈37 POWERS OF TEN", 25, SAND, BOLD, 3.8).move_to(DOWN*1.75)
            self.play(FadeIn(atom), FadeIn(nucleus), run_time=0.55)
            self.play(Create(path), FadeIn(galaxy), run_time=0.8)
            self.play(FadeIn(headline), FadeIn(punch), run_time=0.55)
            self.wait(0.7)
            self.play(FadeOut(atom), FadeOut(nucleus), FadeOut(path), FadeOut(galaxy),
                      FadeOut(headline), FadeOut(punch), run_time=0.35)

        elif is_voyager:
            earth = Circle(
                radius=0.48, color="#4A9AC2",
                fill_color="#164A70", fill_opacity=1
            ).move_to(LEFT * 0.95 + UP * 0.55)
            probe = voyager_probe_sprite(0.075).move_to(LEFT * 0.05 + UP * 0.55)
            record = voyager_record_sprite(0.34).move_to(RIGHT * 1.05 + UP * 0.55)
            path = DashedLine(LEFT * 0.42 + UP * 0.55, RIGHT * 0.62 + UP * 0.55,
                              color=TEAL, stroke_width=2)
            cold_open = fit_paragraph(
                "A MESSAGE FROM EARTH, PACKED ON A RECORD AND SENT INTO DEEP SPACE.",
                29, SAND, max_width=4.0
            ).move_to(DOWN * 1.45)
            self.play(FadeIn(earth), FadeIn(probe), Create(path), run_time=0.7)
            self.play(FadeIn(record), FadeIn(cold_open), run_time=0.7)
            self.play(probe.animate.shift(RIGHT * 0.25), record.animate.scale(1.08),
                      run_time=0.9, rate_func=smooth)
            self.wait(1.0)
            self.play(FadeOut(earth), FadeOut(probe), FadeOut(path),
                      FadeOut(record), FadeOut(cold_open), run_time=0.4)

        elif is_neptune:
            orbit = Ellipse(width=3.2, height=1.45, color="#6B879D", stroke_width=3).move_to(UP*0.55)
            uranus = pixel_sprite(["..BBBB..", ".BBBBBB.", "BBBBBBBB", ".BBBBBB.", "..BBBB.."],
                                  {"B": "#72C4D8"}, pixel=0.10).move_to(LEFT*0.85+UP*0.55)
            neptune = pixel_sprite(["..NNN..", ".NNNNN.", "NNNNNNN", ".NNNNN.", "..NNN.."],
                                   {"N": "#3E79C8"}, pixel=0.10).move_to(RIGHT*1.0+UP*0.55)
            prediction = DashedLine(LEFT*0.15+UP*0.55, RIGHT*0.55+UP*0.55, color=SAND, stroke_width=3)
            cold_open = fit_paragraph(
                "A PLANET PREDICTED BY MATHS—THEN FOUND IN THE SKY.",
                29, SAND, max_width=4.0
            ).move_to(DOWN*1.35)
            self.play(Create(orbit), FadeIn(uranus), run_time=0.65)
            self.play(Create(prediction), FadeIn(neptune), FadeIn(cold_open), run_time=0.8)
            self.wait(1.0)
            self.play(FadeOut(orbit), FadeOut(uranus), FadeOut(neptune),
                      FadeOut(prediction), FadeOut(cold_open), run_time=0.4)

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
            elif lesson.get("title", "").startswith("Great Zimbabwe:"):
                great_zimbabwe_pixel_story(self, index, step)
            elif lesson.get("title", "").startswith("The Antikythera Mechanism:"):
                antikythera_pixel_story(self, index, step)
            elif is_hubble:
                hubble_pixel_story(self, index, step)
            elif is_black_hole:
                black_hole_pixel_story(self, index, step)
            elif is_voyager:
                voyager_pixel_story(self, index, step)
            elif is_scale:
                atom_to_galaxy_scale_story(self, index, step)
            elif lesson.get("id") in ("gps-satellite-navigation", "bioluminescence-ocean", "roman-concrete", "moon-phases", "deep-ocean-pressure", "neptune-math-discovery"):
                modern_topic_visual(self, lesson.get("id"), index)
                number = fit_line(f"DISCOVERY {index}", 23, TEAL, BOLD)
                heading = fit_paragraph(step["heading"], 34, SAND)
                body = fit_paragraph(step["body"], 27, WHITE)
                card = VGroup(number, heading, body).arrange(DOWN, buff=0.35).move_to(DOWN * 2.2)
                self.play(FadeIn(card, shift=UP * 0.12), run_time=0.55)
                self.wait(2.5)
                self.play(FadeOut(card), run_time=0.3)
            elif lesson.get("title", "").startswith("Lightning Explained:"):
                lightning_physics_story(self, index, step)
            elif lesson.get("title", "").startswith("Why Is the Sky Blue:"):
                sky_blue_pixel_story(self, index, step)
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
        elif is_hubble:
            end_card = VGroup(
                fit_line("FIVE SPACEWALKS. A CLEARER VIEW.", 22, SAND, BOLD, max_width=4.0),
                fit_line("STS-61 • DECEMBER 1993", 20, WHITE, BOLD),
            ).arrange(DOWN, buff=0.28).move_to(UP * 0.6)
            self.play(FadeIn(end_card), run_time=0.6)
            self.wait(0.7)
            self.play(FadeOut(end_card), run_time=0.35)
        elif is_black_hole:
            end_card = VGroup(
                fit_line("EIGHT TELESCOPES. ONE SHARED IMAGE.", 22, SAND, BOLD, max_width=4.0),
                fit_line("M87* • REVEALED 10 APRIL 2019", 20, WHITE, BOLD),
            ).arrange(DOWN, buff=0.28).move_to(UP * 0.6)
            self.play(FadeIn(end_card), run_time=0.6)
            self.wait(0.7)
            self.play(FadeOut(end_card), run_time=0.35)

        elif is_voyager:
            end_card = VGroup(
                fit_line("ONE PLANET'S HELLO. TWO VOYAGER PROBES.", 21, SAND, BOLD, max_width=4.0),
                fit_line("THE GOLDEN RECORD • 1977", 20, WHITE, BOLD),
            ).arrange(DOWN, buff=0.28).move_to(UP * 0.6)
            self.play(FadeIn(end_card), run_time=0.6)
            self.wait(0.8)
            self.play(FadeOut(end_card), run_time=0.35)

        if is_neptune:
            end_card = VGroup(
                fit_line("MATHS PREDICTED IT. A TELESCOPE CONFIRMED IT.", 20, SAND, BOLD, max_width=4.0),
                fit_line("NEPTUNE • 23 SEPTEMBER 1846", 20, WHITE, BOLD),
            ).arrange(DOWN, buff=0.28).move_to(UP * 0.6)
            self.play(FadeIn(end_card), run_time=0.6)
            self.wait(0.8)
            self.play(FadeOut(end_card), run_time=0.35)

        outro = VGroup(
            fit_line("MISSION COMPLETE!", 32, SAND, BOLD),
            fit_paragraph("Explore • Learn • Create", 30, WHITE),
            fit_paragraph("Try the lesson and quiz at Adventure Academy.", 25, TEAL),
        ).arrange(DOWN, buff=0.48).move_to(ORIGIN)
        self.play(FadeIn(outro), run_time=0.8)
        self.wait(2.5)

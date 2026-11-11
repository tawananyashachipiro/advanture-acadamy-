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
    body = fit_paragraph(step["body"], 20, WHITE, max_width=3.95)
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
            elif lesson.get("title", "").startswith("Lightning Explained:"):
                lightning_physics_story(self, index, step)
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
        outro = VGroup(
            fit_line("MISSION COMPLETE!", 32, SAND, BOLD),
            fit_paragraph("Explore • Learn • Create", 30, WHITE),
            fit_paragraph("Try the lesson and quiz at Adventure Academy.", 25, TEAL),
        ).arrange(DOWN, buff=0.48).move_to(ORIGIN)
        self.play(FadeIn(outro), run_time=0.8)
        self.wait(2.5)

#!/usr/bin/env python3
"""Build a reviewed, YouTube-Shorts-ready Adventure Academy lesson package."""
import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "creator-studio" / "lessons" / "curriculum.json"
SCENE = ROOT / "creator-studio" / "scenes" / "lesson_short.py"
DIST = ROOT / "creator-studio" / "dist"


def slug_ok(value):
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value))


def stamp(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def make_srt(lesson, duration=None):
    """Create captions from the spoken script and pace them to the audio length."""
    words = lesson["voiceover"].strip().split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) >= 5 or word.endswith((".", "?", "!")):
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    total_words = max(1, len(words))
    duration = duration or (total_words / 2.35)
    entries = []
    cursor = 0.0
    for chunk in chunks:
        chunk_words = len(chunk.split())
        end = cursor + duration * chunk_words / total_words
        entries.append((cursor, end, chunk))
        cursor = end
    return "\n\n".join(
        f"{i}\n{stamp(start)} --> {stamp(end)}\n{text}"
        for i, (start, end, text) in enumerate(entries, 1)
    ) + "\n"



def download_apollo_photos(out):
    """Download official NASA Apollo 13 archive images for the Apollo lesson only."""
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    images = {
        "launch.jpg": "S70-34852",
        "mission-control.jpg": "S70-34902",
        "earth-return.jpg": "as13-60-8588",
        "splashdown.jpg": "S70-35638",
    }
    for filename, nasa_id in images.items():
        target = assets / filename
        if target.exists() and target.stat().st_size > 20_000:
            continue
        url = f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~large.jpg"
        request = urllib.request.Request(url, headers={"User-Agent": "AdventureAcademyClipFactory/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response, target.open("wb") as output:
            shutil.copyfileobj(response, output)
        if target.stat().st_size < 20_000:
            raise RuntimeError(f"NASA image download looks incomplete: {nasa_id}")
    return assets


def download_lightning_photo(out):
    """Fetch a public-domain NOAA lightning photograph from Wikimedia Commons."""
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    target = assets / "lightning-noaa.jpg"
    if target.exists() and target.stat().st_size > 50_000:
        return assets
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/Lightning_NOAA.jpg"
    request = urllib.request.Request(url, headers={"User-Agent": "AdventureAcademyClipFactory/1.0 (educational video)"})
    with urllib.request.urlopen(request, timeout=45) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)
    if target.stat().st_size < 50_000:
        raise RuntimeError("Lightning photograph download is incomplete.")
    return assets



def make_background_music(duration, destination):
    """Generate a quiet, original ambient pad without external music assets."""
    import wave
    import numpy as np
    sample_rate = 44100
    count = max(1, int(sample_rate * duration))
    t = np.arange(count, dtype=np.float64) / sample_rate
    notes = (130.81, 164.81, 196.00, 261.63)
    signal = sum(np.sin(2 * np.pi * hz * t + phase)
                 for hz, phase in zip(notes, (0.0, 0.7, 1.4, 2.1))) / len(notes)
    pulse = 0.78 + 0.22 * np.sin(2 * np.pi * 0.075 * t)
    fade_in = np.minimum(1.0, t / 1.8)
    fade_out = np.minimum(1.0, np.maximum(0.0, (duration - t) / 2.2))
    mono = signal * pulse * fade_in * fade_out * 0.12
    stereo = np.column_stack((mono, mono))
    pcm = np.clip(stereo * 32767, -32768, 32767).astype("<i2")
    with wave.open(str(destination), "wb") as audio:
        audio.setnchannels(2)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(pcm.tobytes())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", required=True, help="Lesson ID from curriculum.json")
    args = parser.parse_args()
    if not slug_ok(args.lesson):
        raise SystemExit("Invalid lesson ID. Use lowercase letters, numbers and hyphens only.")

    curriculum = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    if args.lesson not in curriculum:
        raise SystemExit(f"Unknown lesson '{args.lesson}'. Check creator-studio/lessons/curriculum.json.")
    lesson = curriculum[args.lesson]
    if len(lesson.get("options", [])) < 2 or not (0 <= lesson.get("answer_index", -1) < len(lesson["options"])):
        raise SystemExit("Lesson quiz is incomplete or has an invalid answer_index.")
    if len(lesson.get("steps", [])) < 2:
        raise SystemExit("A lesson needs at least two discovery steps.")

    out = DIST / args.lesson
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    active = out / "active-lesson.json"
    assets = (download_apollo_photos(out) if args.lesson == "apollo-13-rescue" else
              download_lightning_photo(out) if args.lesson == "physics-lightning-explained" else None)
    active.write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")

    quiz = {
        "lesson_id": args.lesson,
        "subject": lesson["subject"],
        "title": lesson["title"],
        "question": lesson["question"],
        "options": lesson["options"],
        "correct_option_index": lesson["answer_index"],
        "correct_answer": lesson["options"][lesson["answer_index"]],
        "explanation": lesson["explanation"],
    }
    (out / "quiz.json").write_text(json.dumps(quiz, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "voiceover-script.txt").write_text(lesson["voiceover"].strip() + "\n", encoding="utf-8")
    (out / "captions.srt").write_text(make_srt(lesson), encoding="utf-8")

    hashtags = " ".join(lesson.get("hashtags", ["#AdventureOfEducation", "#LearnWithMe", "#Education", "#" + re.sub(r"[^A-Za-z0-9]", "", lesson["subject"].title())]))
    sources = lesson.get("sources", [])
    source_lines = [f"- {source['organization']}: {source['title']} — {source['url']}" for source in sources]
    sources_text = "Sources checked:\n" + "\n".join(source_lines) if source_lines else "No source list supplied for this lesson."
    if sources:
        (out / "sources.txt").write_text(sources_text + "\n", encoding="utf-8")
    fact_check_notes = lesson.get("fact_check_notes")
    if fact_check_notes:
        (out / "FACT-CHECK-NOTES.txt").write_text(fact_check_notes.strip() + "\n", encoding="utf-8")
    thumbnail_guidance = lesson.get("thumbnail_guidance")
    if thumbnail_guidance:
        (out / "thumbnail-guidance.txt").write_text(thumbnail_guidance.strip() + "\n", encoding="utf-8")

    description = (
        f"{lesson['title']}\n\n{lesson['concept']}\n\n"
        "Pause at the challenge, choose your answer, then watch the explanation. "
        "Continue learning with the matching lesson and quiz at Adventure Academy: "
        "https://tawananyashachipiro.github.io/advanture-acadamy-/\n\n"
        f"{sources_text}\n\n"
        f"{hashtags}\n\n"
        "Educational content: review the lesson, sources and captions before publishing."
    )
    metadata = {
        "lesson_id": args.lesson,
        "title": lesson["title"],
        "subject": lesson["subject"],
        "format": "YouTube Shorts vertical 9:16",
        "description": description,
        "hashtags": hashtags,
        "sources": sources,
        "hook": lesson.get("hook"),
        "fact_check_notes": fact_check_notes,
        "thumbnail_guidance": thumbnail_guidance,
        "review_before_publishing": True,
        "publishing": "Manual upload after channel-owner review; no credentials stored in GitHub.",
    }
    (out / "youtube-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "youtube-description.txt").write_text(description + "\n", encoding="utf-8")

    pinned_comment = lesson.get("pinned_comment")
    if pinned_comment:
        (out / "pinned-comment.txt").write_text(pinned_comment + "\n", encoding="utf-8")
    metadata["pinned_comment"] = pinned_comment
    (out / "youtube-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


    if args.lesson == "physics-lightning-explained":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#07172D"/><stop offset="1" stop-color="#234A68"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="18" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="1280" height="720" fill="url(#sky)"/>
<g fill="#526D83"><ellipse cx="350" cy="245" rx="230" ry="105"/><ellipse cx="515" cy="190" rx="190" ry="130"/><ellipse cx="690" cy="260" rx="245" ry="110"/></g>
<path d="M640 260 L530 430 L635 420 L555 650 L820 365 L690 385 L785 260 Z" fill="#FFD45C" stroke="#FFF4C6" stroke-width="12" filter="url(#glow)"/>
<text x="75" y="90" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="40" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="75" y="590" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="72" font-weight="bold">LIGHTNING!</text>
<text x="80" y="660" fill="#FFD45C" font-family="Arial,sans-serif" font-size="36" font-weight="bold">THE SCIENCE BEHIND THE FLASH</text>
</svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
    elif args.lesson == "why-sky-blue":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#07172D"/><stop offset="1" stop-color="#1676B8"/></linearGradient></defs>
<rect width="1280" height="720" fill="url(#sky)"/><circle cx="1010" cy="180" r="105" fill="#FFD27A"/>
<g stroke-width="12" stroke-linecap="round"><path d="M900 220L650 360" stroke="#65C5FF"/><path d="M900 250L670 450" stroke="#65C5FF"/><path d="M900 280L760 520" stroke="#65C5FF"/><path d="M890 190L620 260" stroke="#FFFFFF"/></g>
<text x="72" y="110" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="40" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="72" y="430" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="94" font-weight="bold">WHY IS THE</text>
<text x="72" y="535" fill="#FFD27A" font-family="Arial,sans-serif" font-size="112" font-weight="bold">SKY BLUE?</text>
<text x="78" y="625" fill="#D8F1EC" font-family="Arial,sans-serif" font-size="34">THE SCIENCE OF SCATTERED LIGHT</text></svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
        from PIL import Image, ImageDraw, ImageFont
        thumb = Image.new("RGB", (1280, 720), (7, 23, 45))
        draw = ImageDraw.Draw(thumb)
        for y in range(720):
            blend = y / 720
            draw.line((0, y, 1280, y),
                      fill=(int(7 + 15*blend), int(23 + 90*blend), int(45 + 145*blend)))
        draw.ellipse((895, 65, 1125, 295), fill=(255, 190, 85))
        try:
            font_brand = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
            font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except OSError:
            font_brand = font_title = font_sub = ImageFont.load_default()
        draw.text((72, 80), "ADVENTURE OF EDUCATION", font=font_brand, fill=(139,226,210))
        draw.text((72, 360), "WHY IS THE", font=font_title, fill="white", stroke_width=3, stroke_fill=(4,18,35))
        draw.text((72, 465), "SKY BLUE?", font=font_title, fill=(255,210,122), stroke_width=3, stroke_fill=(4,18,35))
        draw.text((78, 610), "THE SCIENCE OF SCATTERED LIGHT", font=font_sub, fill=(216,241,236))
        thumb.save(out / "thumbnail.jpg", quality=94)
    elif args.lesson == "hubble-repair-mission":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="space" x2="0" y2="1"><stop stop-color="#06172B"/><stop offset="1" stop-color="#163A59"/></linearGradient></defs>
<rect width="1280" height="720" fill="url(#space)"/>
<g fill="#D8F1EC" opacity=".8"><circle cx="105" cy="180" r="4"/><circle cx="330" cy="110" r="5"/><circle cx="560" cy="230" r="3"/><circle cx="1120" cy="160" r="5"/><circle cx="990" cy="510" r="4"/><circle cx="760" cy="95" r="3"/></g>
<g stroke="#D8F1EC" stroke-width="7" fill="none"><rect x="770" y="235" width="260" height="82" rx="8" fill="#AFC2D1"/><rect x="650" y="220" width="105" height="112" fill="#1D5C7A"/><rect x="1045" y="220" width="105" height="112" fill="#1D5C7A"/></g>
<g fill="#72C9D8"><path d="M665 230h76v12h-76zm0 28h76v12h-76zm0 28h76v12h-76zm392-56h76v12h-76zm0 28h76v12h-76zm0 28h76v12h-76z"/></g>
<g fill="#FFFFFF" stroke="#0F2238" stroke-width="5"><circle cx="540" cy="300" r="42"/><rect x="510" y="342" width="60" height="120" rx="12"/><path d="M510 375l-60 60 18 18 65-47zm60 0l58 58-18 18-62-45z"/></g>
<text x="70" y="92" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="38" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="70" y="545" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="78" font-weight="bold">FIXING HUBBLE</text>
<text x="74" y="625" fill="#FFD27A" font-family="Arial,sans-serif" font-size="42" font-weight="bold">IN SPACE • FIVE SPACEWALKS</text>
</svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
    elif args.lesson == "black-hole-first-image":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="space" x2="0" y2="1"><stop stop-color="#06101F"/><stop offset="1" stop-color="#17314B"/></linearGradient></defs>
<rect width="1280" height="720" fill="url(#space)"/>
<g fill="#D8F1EC" opacity=".8"><circle cx="95" cy="190" r="4"/><circle cx="330" cy="125" r="5"/><circle cx="610" cy="205" r="3"/><circle cx="1180" cy="115" r="4"/><circle cx="1080" cy="600" r="4"/><circle cx="735" cy="95" r="3"/></g>
<circle cx="965" cy="360" r="185" fill="none" stroke="#FFD58C" stroke-width="7" opacity=".5"/>
<circle cx="965" cy="360" r="150" fill="none" stroke="#FF9D52" stroke-width="42"/>
<circle cx="965" cy="360" r="91" fill="#020611"/>
<g fill="#8BE2D2"><circle cx="965" cy="150" r="8"/><circle cx="1175" cy="360" r="8"/><circle cx="965" cy="570" r="8"/><circle cx="755" cy="360" r="8"/></g>
<text x="72" y="92" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="38" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="72" y="345" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="76" font-weight="bold">FIRST BLACK</text>
<text x="72" y="440" fill="#FFD27A" font-family="Arial,sans-serif" font-size="86" font-weight="bold">HOLE IMAGE</text>
<text x="78" y="575" fill="#D8F1EC" font-family="Arial,sans-serif" font-size="31">8 TELESCOPES • ONE PLANET-SIZED EYE</text>
</svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
        from PIL import Image, ImageDraw, ImageFont
        thumb = Image.new("RGB", (1280, 720), (6, 16, 31))
        draw = ImageDraw.Draw(thumb)
        for y in range(720):
            blend = y / 720
            draw.line((0, y, 1280, y),
                      fill=(int(6 + 18*blend), int(16 + 33*blend), int(31 + 44*blend)))
        for x, y, radius in [(95, 190, 4), (330, 125, 5), (610, 205, 3),
                             (1180, 115, 4), (1080, 600, 4), (735, 95, 3)]:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(216,241,236))
        draw.ellipse((780, 175, 1150, 545), outline=(255,213,140), width=8)
        draw.ellipse((815, 210, 1115, 510), outline=(255,157,82), width=42)
        draw.ellipse((875, 270, 1055, 450), fill=(2,6,17))
        try:
            font_brand = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
            font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except OSError:
            font_brand = font_title = font_sub = ImageFont.load_default()
        draw.text((72, 68), "ADVENTURE OF EDUCATION", font=font_brand, fill=(139,226,210))
        draw.text((72, 300), "FIRST BLACK", font=font_title, fill="white",
                  stroke_width=3, stroke_fill=(4,18,35))
        draw.text((72, 395), "HOLE IMAGE", font=font_title, fill=(255,210,122),
                  stroke_width=3, stroke_fill=(4,18,35))
        draw.text((78, 570), "8 TELESCOPES • ONE PLANET-SIZED EYE",
                  font=font_sub, fill=(216,241,236))
        thumb.save(out / "thumbnail.jpg", quality=94)
    elif args.lesson == "voyager-golden-record":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="space" x2="0" y2="1"><stop stop-color="#061326"/><stop offset="1" stop-color="#173B5A"/></linearGradient></defs>
<rect width="1280" height="720" fill="url(#space)"/>
<g fill="#D8F1EC"><circle cx="90" cy="170" r="4"/><circle cx="340" cy="100" r="5"/><circle cx="650" cy="170" r="3"/><circle cx="1170" cy="130" r="4"/><circle cx="1080" cy="610" r="4"/></g>
<circle cx="980" cy="365" r="178" fill="#C99532" stroke="#FFE7A8" stroke-width="10"/>
<circle cx="980" cy="365" r="142" fill="none" stroke="#F7D77E" stroke-width="3"/>
<circle cx="980" cy="365" r="100" fill="none" stroke="#F7D77E" stroke-width="3"/>
<circle cx="980" cy="365" r="18" fill="#8A5A22"/>
<g fill="#DCE8EF"><rect x="720" y="250" width="20" height="180"/><rect x="640" y="285" width="70" height="110" fill="#2F9E92"/><rect x="750" y="285" width="70" height="110" fill="#2F9E92"/></g>
<text x="70" y="92" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="38" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="70" y="310" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="70" font-weight="bold">EARTH'S MESSAGE</text>
<text x="70" y="405" fill="#FFD27A" font-family="Arial,sans-serif" font-size="76" font-weight="bold">TO THE STARS</text>
<text x="76" y="575" fill="#D8F1EC" font-family="Arial,sans-serif" font-size="34">THE GOLDEN RECORD • 1977</text>
</svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
        from PIL import Image, ImageDraw, ImageFont
        thumb = Image.new("RGB", (1280, 720), (6, 19, 38))
        draw = ImageDraw.Draw(thumb)
        for x, y, radius in [(90, 170, 4), (340, 100, 5), (650, 170, 3),
                             (1170, 130, 4), (1080, 610, 4)]:
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(216,241,236))
        draw.ellipse((802, 187, 1158, 543), fill=(201,149,50), outline=(255,231,168), width=10)
        draw.ellipse((838, 223, 1122, 507), outline=(247,215,126), width=3)
        draw.ellipse((878, 263, 1082, 467), outline=(247,215,126), width=3)
        draw.ellipse((962, 347, 998, 383), fill=(138,90,34))
        draw.rectangle((680, 250, 704, 440), fill=(220,232,239))
        draw.rectangle((600, 285, 670, 395), fill=(47,158,146))
        draw.rectangle((714, 285, 784, 395), fill=(47,158,146))
        try:
            font_brand = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
            font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except OSError:
            font_brand = font_title = font_sub = ImageFont.load_default()
        draw.text((70, 68), "ADVENTURE OF EDUCATION", font=font_brand, fill=(139,226,210))
        draw.text((70, 245), "EARTH'S MESSAGE", font=font_title, fill="white",
                  stroke_width=3, stroke_fill=(4,18,35))
        draw.text((70, 335), "TO THE STARS", font=font_title, fill=(255,210,122),
                  stroke_width=3, stroke_fill=(4,18,35))
        draw.text((76, 575), "THE GOLDEN RECORD • 1977", font=font_sub, fill=(216,241,236))
        thumb.save(out / "thumbnail.jpg", quality=94)
    elif args.lesson == "atom-to-galaxy-scale":
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="space" x2="1" y2="1"><stop stop-color="#061225"/><stop offset=".58" stop-color="#102C4B"/><stop offset="1" stop-color="#261B46"/></linearGradient><radialGradient id="sun"><stop stop-color="#FFF0B2"/><stop offset=".65" stop-color="#FFB14F"/><stop offset="1" stop-color="#E65E45"/></radialGradient></defs>
<rect width="1280" height="720" fill="url(#space)"/>
<g fill="#D9F2FF" opacity=".8"><circle cx="85" cy="190" r="4"/><circle cx="340" cy="105" r="3"/><circle cx="610" cy="190" r="4"/><circle cx="1180" cy="110" r="4"/><circle cx="1080" cy="600" r="3"/><circle cx="780" cy="90" r="3"/><circle cx="210" cy="565" r="4"/></g>
<g transform="translate(185 390)"><circle r="105" fill="#44C1D8" opacity=".12"/><circle r="77" fill="none" stroke="#55C5E6" stroke-width="5" opacity=".8"/><circle r="10" fill="#FFD27A"/><circle cx="75" cy="5" r="9" fill="#FFFFFF"/><circle cx="-18" cy="-73" r="8" fill="#FFFFFF"/></g>
<g transform="translate(650 390)"><circle r="100" fill="#FFB24D" opacity=".13"/><circle r="83" fill="url(#sun)"/><path d="M0 -128V-104M0 104V128M-128 0H-104M104 0H128M-90 -90L-73 -73M90 90L73 73M90 -90L73 -73M-90 90L-73 73" stroke="#FFD27A" stroke-width="9" stroke-linecap="round"/></g>
<g transform="translate(1030 385)" fill="none" stroke="#8BD8F0"><ellipse rx="150" ry="60" stroke-width="7" transform="rotate(-18)"/><ellipse rx="120" ry="49" stroke-width="5" transform="rotate(38)"/></g>
<g transform="translate(1030 385)" fill="#FFE2A5"><circle r="25"/><circle cx="-82" cy="-18" r="7"/><circle cx="76" cy="19" r="6"/><circle cx="25" cy="-44" r="5"/><circle cx="-40" cy="37" r="5"/></g>
<text x="72" y="82" fill="#8BE2D2" font-family="Arial,sans-serif" font-size="34" font-weight="bold" letter-spacing="3">ADVENTURE OF EDUCATION</text>
<text x="72" y="630" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="92" font-weight="bold">37 POWERS OF TEN</text>
<text x="76" y="680" fill="#FFD27A" font-family="Arial,sans-serif" font-size="27" font-weight="bold">FROM AN ATOM TO THE OBSERVABLE UNIVERSE</text>
</svg>"""
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")
        from PIL import Image, ImageDraw, ImageFont
        thumb = Image.new("RGB", (1280, 720), (6, 18, 38))
        draw = ImageDraw.Draw(thumb)
        for y in range(720):
            t = y / 720
            draw.line((0, y, 1280, y),
                      fill=(int(6+18*t), int(18+25*t), int(38+42*t)))
        for x, y, r in [(85,190,4),(340,105,3),(610,190,4),(1180,110,4),
                        (1080,600,3),(780,90,3),(210,565,4)]:
            draw.ellipse((x-r,y-r,x+r,y+r), fill=(220,242,255))
        # Original vector-style icons: atom, Sun and spiral galaxy.
        draw.ellipse((95,300,275,480), outline=(85,197,230), width=8)
        draw.ellipse((172,377,198,403), fill=(255,210,122))
        draw.ellipse((255,380,273,398), fill=(255,255,255))
        draw.ellipse((565,300,735,470), fill=(255,179,79), outline=(255,220,145), width=5)
        draw.ellipse((590,325,710,445), fill=(255,195,100))
        for angle in range(0,360,45):
            import math
            import numpy as np
            x1=650+100*math.cos(math.radians(angle)); y1=385+100*math.sin(math.radians(angle))
            x2=650+122*math.cos(math.radians(angle)); y2=385+122*math.sin(math.radians(angle))
            draw.line((x1,y1,x2,y2), fill=(255,210,122), width=5)
        for j in range(26):
            import math
            a=j*0.55; radius=8+j*4.5
            x=1030+radius*math.cos(a); y=385+radius*0.5*math.sin(a)
            draw.ellipse((x-3,y-3,x+3,y+3), fill=(255,225,175) if j%3==0 else (135,216,240))
        try:
            brand_font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",34)
            title_font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",82)
            sub_font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",25)
        except OSError:
            brand_font=title_font=sub_font=ImageFont.load_default()
        draw.text((72,78),"ADVENTURE OF EDUCATION",font=brand_font,fill=(139,226,210))
        draw.text((72,565),"37 POWERS OF TEN",font=title_font,fill=(255,255,255),
                  stroke_width=4,stroke_fill=(4,16,32))
        draw.text((76,666),"ATOM → OBSERVABLE UNIVERSE",font=sub_font,fill=(255,210,122))
        thumb.save(out / "thumbnail.jpg", quality=95, subsampling=0)
    else:
        title = escape(lesson["subject"].upper())
        subtitle = escape(lesson["title"])
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<rect width="1280" height="720" fill="#0F2238"/>
<circle cx="1080" cy="120" r="210" fill="#2F9E92" opacity=".25"/>
<circle cx="150" cy="650" r="260" fill="#FFD27A" opacity=".15"/>
<text x="90" y="150" fill="#2F9E92" font-family="Arial,sans-serif" font-size="42" font-weight="bold">ADVENTURE OF EDUCATION</text>
<text x="90" y="310" fill="#FFD27A" font-family="Arial,sans-serif" font-size="48" font-weight="bold">{title}</text>
<text x="90" y="420" fill="#FFFFFF" font-family="Arial,sans-serif" font-size="54" font-weight="bold">{subtitle}</text>
<text x="90" y="610" fill="#D8F1EC" font-family="Arial,sans-serif" font-size="34">PAUSE • THINK • DISCOVER</text>
</svg>'''
        (out / "thumbnail.svg").write_text(svg, encoding="utf-8")

    if args.lesson == "physics-lightning-explained":
        from PIL import Image, ImageDraw, ImageFont
        photo = Image.open(assets / "lightning-noaa.jpg").convert("RGB")
        target_ratio = 16 / 9
        width, height = photo.size
        if width / height > target_ratio:
            crop_w = int(height * target_ratio)
            left = (width - crop_w) // 2
            photo = photo.crop((left, 0, left + crop_w, height))
        else:
            crop_h = int(width / target_ratio)
            top = (height - crop_h) // 2
            photo = photo.crop((0, top, width, top + crop_h))
        photo = photo.resize((1280, 720))
        overlay = Image.new("RGBA", photo.size, (3, 15, 32, 105))
        photo = Image.alpha_composite(photo.convert("RGBA"), overlay)
        draw = ImageDraw.Draw(photo)
        draw.rectangle((0, 0, 1280, 112), fill=(3, 15, 32, 190))
        draw.text((58, 35), "ADVENTURE OF EDUCATION", fill=(139, 226, 210, 255))
        draw.text((58, 475), "LIGHTNING!", fill=(255, 255, 255, 255),
                  stroke_width=3, stroke_fill=(4, 18, 35, 255))
        draw.text((62, 565), "THE SCIENCE BEHIND THE FLASH",
                  fill=(255, 212, 92, 255), stroke_width=2,
                  stroke_fill=(4, 18, 35, 255))
        photo.convert("RGB").save(out / "thumbnail.jpg", quality=92)

    (out / "REVIEW-CHECKLIST.txt").write_text(
        "Before uploading:\n"
        "[ ] Watch the complete MP4.\n"
        "[ ] Check all subject facts and spelling.\n"
        "[ ] Record or add the supplied voice-over script if narration is wanted.\n"
        "[ ] Proofread captions and check timing.\n"
        "[ ] Confirm you own or have permission for every added asset.\n"
        "[ ] Check YouTube title, description, audience and visibility.\n"
        "[ ] Upload manually only after approval.\n",
        encoding="utf-8",
    )

    env = dict(__import__("os").environ)
    env["ACADEMY_LESSON_FILE"] = str(active)
    if assets:
        env["ACADEMY_ASSET_DIR"] = str(assets)
    media = out / "render"
    command = [
        sys.executable, "-m", "manim", "-qh",
        "--resolution", "1080,1920",
        "--media_dir", str(media),
        "--output_file", "AdventureAcademyShort",
        str(SCENE), "AcademyLessonShort",
    ]
    subprocess.run(command, cwd=ROOT, env=env, check=True)
    videos = list(media.rglob("AdventureAcademyShort.mp4"))
    if not videos:
        videos = list(media.rglob("*.mp4"))
    if not videos:
        raise SystemExit("Manim completed but no MP4 was found.")
    final_video = out / "AdventureAcademyShort.mp4"
    shutil.copy2(videos[0], final_video)

    # Prefer a free, offline Piper neural voice for warmer, more natural narration.
    # Fall back to a slower, softer eSpeak voice if the model cannot be fetched.
    espeak = shutil.which("espeak-ng")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is missing.")
    silent_video = out / "AdventureAcademyShort-silent.mp4"
    shutil.copy2(final_video, silent_video)
    voice_audio = out / "voiceover.wav"
    spoken_script = (out / "voiceover-script.txt").read_text(encoding="utf-8")
    piper_model = out / "en_US-amy-medium.onnx"
    piper_config = out / "en_US-amy-medium.onnx.json"
    try:
        for path, url in [
            (piper_model, "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx"),
            (piper_config, "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json"),
        ]:
            request = urllib.request.Request(url, headers={"User-Agent": "AdventureAcademyClipFactory/1.0"})
            with urllib.request.urlopen(request, timeout=60) as response, path.open("wb") as output:
                shutil.copyfileobj(response, output)
        subprocess.run([
            sys.executable, "-m", "piper", "--model", str(piper_model),
            "--output_file", str(voice_audio), "--length-scale", "1.12",
            "--sentence-silence", "0.28",
        ], input=spoken_script, text=True, cwd=ROOT, check=True)
        (out / "voiceover-engine.txt").write_text(
            "Piper neural voice: en_US-amy-medium (offline, open-source model).\n",
            encoding="utf-8",
        )
    except Exception as error:
        if not espeak:
            raise SystemExit(f"Offline voice setup failed and eSpeak NG is unavailable: {error}")
        subprocess.run([
            espeak, "-v", "en-us+f3", "-s", "132", "-a", "112", "-p", "43",
            "-f", str(out / "voiceover-script.txt"), "-w", str(voice_audio)
        ], cwd=ROOT, check=True)
        (out / "voiceover-engine.txt").write_text(
            "Fallback voice: eSpeak NG, slower and softer settings; still synthetic.\n",
            encoding="utf-8",
        )
    audio_seconds = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(voice_audio)
    ], text=True).strip())
    (out / "captions.srt").write_text(make_srt(lesson, audio_seconds), encoding="utf-8")
    voiced_video = out / "AdventureAcademyShort-voiced.mp4"
    silent_seconds = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(silent_video)
    ], text=True).strip())
    target_seconds = max(audio_seconds, silent_seconds)
    music_audio = out / "background-music.wav"
    make_background_music(target_seconds, music_audio)
    pad_seconds = max(0.0, target_seconds - silent_seconds)

    # Original ambient music is mixed quietly beneath the complete narration.
    subprocess.run([
        ffmpeg, "-y", "-i", str(silent_video), "-i", str(voice_audio),
        "-i", str(music_audio),
        "-map", "0:v:0",
        "-filter_complex",
        "[1:a]volume=1.0[voice];[2:a]volume=0.15[music];"
        "[voice][music]amix=inputs=2:duration=longest:dropout_transition=2[a]",
        "-map", "[a]",
        "-vf", f"tpad=stop_mode=clone:stop_duration={pad_seconds:.3f},"
               "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,"
               f"subtitles='{(out / 'captions.srt').resolve().as_posix()}':"
               "force_style='FontName=DejaVu Sans,FontSize=10,Bold=1,PrimaryColour=&H00FFFFFF,"
               "OutlineColour=&H00101828,BorderStyle=1,Outline=2,Shadow=1,"
               "Alignment=2,MarginV=42,MarginL=72,MarginR=175,WrapStyle=2'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{target_seconds:.3f}",
        "-movflags", "+faststart", str(voiced_video)
    ], cwd=ROOT, check=True)

    final_seconds = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(voiced_video)
    ], text=True).strip())
    video_stream = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "json", str(voiced_video)
    ], text=True))["streams"][0]
    if (video_stream["width"], video_stream["height"]) != (1080, 1920):
        raise SystemExit(f"Wrong export dimensions: {video_stream}")
    if video_stream["r_frame_rate"] != "30/1":
        raise SystemExit(f"Wrong export frame rate: {video_stream}")
    if final_seconds < audio_seconds - 0.25:
        raise SystemExit(
            f"Final video ({final_seconds:.2f}s) is shorter than narration "
            f"({audio_seconds:.2f}s); refusing to package a cut-off voice-over."
        )
    print("VIDEO_RESOLUTION=1080x1920")
    print("VIDEO_FPS=30")
    print("BACKGROUND_MUSIC=original ambient bed at 15 percent")
    print("CAPTIONS_BURNED_IN=white text with black outline and mobile-safe margins")
    print(f"VOICEOVER_SECONDS={audio_seconds:.2f}")
    print(f"FINAL_VIDEO_SECONDS={final_seconds:.2f}")
    shutil.move(str(voiced_video), str(final_video))
    shutil.rmtree(media, ignore_errors=True)
    active.unlink(missing_ok=True)
    print(f"PACKAGE_READY={out}")
    print(f"VIDEO={final_video}")


if __name__ == "__main__":
    main()

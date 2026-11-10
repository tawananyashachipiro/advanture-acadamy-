#!/usr/bin/env python3
"""Build a reviewed, YouTube-Shorts-ready Adventure Academy lesson package."""
import argparse
import json
import re
import shutil
import subprocess
import sys
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
        if len(current) >= 8 or word.endswith((".", "?", "!")):
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

    hashtags = "#AdventureOfEducation #LearnWithMe #Education #" + re.sub(r"[^A-Za-z0-9]", "", lesson["subject"].title())
    sources = lesson.get("sources", [])
    source_lines = [f"- {source['organization']}: {source['title']} — {source['url']}" for source in sources]
    sources_text = "Sources checked:\n" + "\n".join(source_lines) if source_lines else "No source list supplied for this lesson."
    if sources:
        (out / "sources.txt").write_text(sources_text + "\n", encoding="utf-8")

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
        "review_before_publishing": True,
        "publishing": "Manual upload after channel-owner review; no credentials stored in GitHub.",
    }
    (out / "youtube-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "youtube-description.txt").write_text(description + "\n", encoding="utf-8")

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
    media = out / "render"
    command = [
        sys.executable, "-m", "manim", "-ql",
        "--resolution", "720,1280",
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

    # Generate a zero-cost offline narration track with eSpeak NG, then mux it
    # into the rendered animation. Keep a silent copy and WAV for review.
    espeak = shutil.which("espeak-ng")
    ffmpeg = shutil.which("ffmpeg")
    if not espeak or not ffmpeg:
        raise SystemExit("Audio tools are missing. Install espeak-ng and ffmpeg.")
    silent_video = out / "AdventureAcademyShort-silent.mp4"
    shutil.copy2(final_video, silent_video)
    voice_audio = out / "voiceover.wav"
    subprocess.run([
        espeak, "-v", lesson.get("voice_language", "en-us"), "-s", "145",
        "-a", "135", "-p", "48", "-f", str(out / "voiceover-script.txt"), "-w", str(voice_audio)
    ], cwd=ROOT, check=True)
    audio_seconds = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(voice_audio)
    ], text=True).strip())
    (out / "captions.srt").write_text(make_srt(lesson, audio_seconds), encoding="utf-8")
    voiced_video = out / "AdventureAcademyShort-voiced.mp4"
    subprocess.run([
        ffmpeg, "-y", "-i", str(silent_video), "-i", str(voice_audio),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "128k", "-af", "apad", "-shortest", "-movflags", "+faststart",
        str(voiced_video)
    ], cwd=ROOT, check=True)
    shutil.move(str(voiced_video), str(final_video))
    shutil.rmtree(media, ignore_errors=True)
    active.unlink(missing_ok=True)
    print(f"PACKAGE_READY={out}")
    print(f"VIDEO={final_video}")


if __name__ == "__main__":
    main()

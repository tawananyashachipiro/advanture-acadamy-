# Adventure Academy Creator Studio

A separate, free/open-source workspace for producing original educational videos. It does not change the live academy website.

## Included tool: Manim Community

[Manim Community](https://github.com/ManimCommunity/manim) creates animated explanations, diagrams, maths and science visuals from Python. It is MIT-licensed and supports MP4 rendering.

### Render on GitHub (no local installation required)

1. Open the repository's **Actions** tab.
2. Select **Render Adventure Academy video**.
3. Select **Run workflow** and confirm.
4. When the run finishes, open it and download the `academy-video` artifact.
5. Preview the MP4 and check every fact, spelling and visual before using it.

The workflow is manual-only. It does not publish anything to YouTube.

### Render on your Mac

Install the system dependencies first:

```bash
brew install cairo pango ffmpeg pkg-config
```

Then from the repository folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r creator-studio/requirements.txt
python -m manim -qm --media_dir creator-studio/output creator-studio/scenes/academy_intro.py AcademyIntro
```

The rendered MP4 is placed under `creator-studio/output/`.

## Suggested free creator tools

- [OBS Studio](https://github.com/obsproject/obs-studio) — record lessons, demonstrations and screen walkthroughs.
- [Kdenlive](https://github.com/KDE/kdenlive) — edit the recordings, add transitions, narration and titles.
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) — create draft subtitles locally; proofread them.
- [Manim Community](https://github.com/ManimCommunity/manim) — create animated subject explanations.

These are separate desktop tools; GitHub Pages cannot run desktop applications inside the academy website.

## YouTube workflow

1. Create original lesson content or use media you have permission to use.
2. Render and review the MP4.
3. Record or create subtitles and proofread them.
4. Upload the finished video through YouTube Studio, using an account that is permitted to manage the channel.
5. Check the title, description, thumbnail, audience setting and visibility before publishing.

The YouTube Data API can upload videos and set metadata, but it requires OAuth authorization. Do not put Google client secrets, access tokens or passwords in this public repository. We have deliberately not enabled automatic publishing.

## Safety and quality checks

- Use only original, public-domain or properly licensed music, images and footage.
- Do not include learner names, faces, email addresses or private progress data in videos.
- Check educational facts and captions before publication.
- Keep generated MP4s out of the website source until they have been reviewed.


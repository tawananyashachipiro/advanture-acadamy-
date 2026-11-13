# Adventure Academy Creator Studio

A separate, free/open-source video workspace for Adventure Academy. It creates original educational lesson clips and a review-ready YouTube publishing pack. It does not change the live academy website.

## Clip Factory (GitHub Actions)

The **Adventure Academy Clip Factory** workflow creates a vertical 9:16 YouTube Short at 1080×1920 and 30 fps for any of the 12 starter lessons in `lessons/curriculum.json`.

### Run it

1. Open the repository's **Actions** tab.
2. Select **Adventure Academy Clip Factory** in the left sidebar.
3. Select **Run workflow**.
4. Choose a lesson from the `lesson_id` list.
5. Start the workflow and wait for the green success check.
6. Open the completed run and download its `academy-clip-...` artifact ZIP.

### Each generated package contains

- `AdventureAcademyShort.mp4` — vertical animated lesson clip, with a pause-and-answer challenge and answer reveal.
- `voiceover-script.txt` — narration text ready for recording.
- `captions.srt` — timed draft captions for review.
- `quiz.json` — question, options, correct answer and explanation, ready for later academy integration.
- `youtube-metadata.json` and `youtube-description.txt` — suggested title, description and hashtags.
- `thumbnail.svg` and `thumbnail.jpg` — editable vector and upload-ready thumbnail artwork.
- `background-music.wav` — original, locally generated ambient music mixed quietly under narration.
- `REVIEW-CHECKLIST.txt` — checks to complete before publishing.

The first 12 lessons cover Biology, Chemistry, Physics, Geography, History, Computer Science, Business Studies, Shona, Art & Design, Mathematics, General Science and Library Skills.

## Add or edit a lesson

Edit `lessons/curriculum.json`. Every lesson needs:
- `subject`, `level`, `title`, `hook`, and `concept`
- At least two `steps`, each with a `heading` and `body`
- A `question`, at least two `options`, a valid `answer_index`, and an `explanation`
- A `voiceover` script

Add the new lesson ID to the workflow's choice list in `.github/workflows/render-academy-video.yml`.

## Safety, permissions and publishing

- The workflow is manual-only. It does not run on every website commit.
- Workflow permissions are read-only for repository contents.
- GitHub Actions are pinned to reviewed release commit SHAs.
- No third-party action is given write permissions or access to YouTube credentials.
- The Clip Factory only builds artifacts. The channel owner uploads the reviewed MP4 manually through YouTube Studio. No upload credentials or OAuth tokens are needed by this video-production workflow.
- Never put passwords, OAuth client secrets, access tokens or private learner data in this repository.
- Use original, public-domain or properly licensed media and music only.
- Review educational content for accuracy before publication.

## Tools used

- [Manim Community](https://github.com/ManimCommunity/manim) — MIT-licensed programmatic animation.
- [FFmpeg](https://ffmpeg.org/) — video processing.
- [GitHub Actions](https://github.com/features/actions) — hosted build automation.

The workflow uses GitHub-hosted runners and the repository's public source. GitHub usage limits and availability still apply; this is not a promise of unlimited free rendering.

## Important current limitation

The generated quiz JSON is a ready-to-integrate content asset; it is not yet connected to the live website's lesson or progress system. The video itself contains an on-screen pause-and-answer moment, not clickable YouTube quiz controls. A future website integration can load the same quiz data into an interactive academy activity.

## Optional MoneyPrinterTurbo finishing pass

The Clip Factory includes an optional, manually selected MoneyPrinterTurbo pass. It is disabled by default to protect the free GitHub Actions allowance.

When running **Adventure Academy Clip Factory**, tick `use_moneyprinterturbo` only if you want an additional render. This mode uses the lesson's existing silent MP4, supplied narration WAV and prepared script as local inputs. It explicitly selects local media, disables automatic voice generation, disables subtitles in this extra pass, and disables background music. It does not request an LLM, Pexels footage, paid video generation, or paid music.

MoneyPrinterTurbo is installed from its official Python package at the pinned version `mpt==1.3.10`. Its output is saved as a separate artifact named `moneyprinterturbo-<lesson-id>`; the original `academy-clip-<lesson-id>` artifact remains unchanged.

This optional pass uses extra GitHub Actions minutes and may take longer. GitHub-hosted runner availability and free usage limits still apply. It has been wired into the workflow but must complete a successful test run before being treated as production-verified. The ordinary Clip Factory remains the default and does not install MoneyPrinterTurbo.



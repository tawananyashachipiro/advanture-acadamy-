#!/usr/bin/env python3
"""Upload a reviewed Adventure Academy artifact to YouTube as PRIVATE only."""
import argparse
import os
import zipfile
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--tags", default="")
    p.add_argument("--made-for-kids", choices=("true", "false"), required=True)
    p.add_argument("--category-id", default="27")
    args = p.parse_args()

    root = Path("youtube_upload_work")
    root.mkdir(exist_ok=True)
    with zipfile.ZipFile(args.artifact) as zf:
        for item in zf.infolist():
            target = (root / item.filename).resolve()
            if root.resolve() not in target.parents and target != root.resolve():
                raise ValueError("Unsafe path in artifact")
        zf.extractall(root)

    videos = list(root.rglob("AdventureAcademyShort.mp4"))
    if len(videos) != 1:
        raise RuntimeError(f"Expected one video, found {len(videos)}")
    video = videos[0]
    thumbnails = list(root.rglob("thumbnail.png")) or list(root.rglob("thumbnail.jpg"))
    captions = list(root.rglob("captions.srt"))
    if not thumbnails:
        raise RuntimeError("No thumbnail.png or thumbnail.jpg found in artifact")
    if not captions:
        raise RuntimeError("No captions.srt found in artifact")

    required = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Missing GitHub Actions secrets: " + ", ".join(missing))

    creds = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.force-ssl"],
    )
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    body = {
        "snippet": {
            "title": args.title[:100],
            "description": args.description,
            "tags": tags,
            "categoryId": args.category_id,
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": args.made_for_kids == "true",
        },
    }
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(video), mimetype="video/mp4", resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()
    video_id = response["id"]
    print(f"PRIVATE_UPLOAD_VIDEO_ID={video_id}")

    thumb = thumbnails[0]
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(
            str(thumb), mimetype="image/png" if thumb.suffix.lower() == ".png" else "image/jpeg"
        ),
    ).execute()
    print("THUMBNAIL_UPLOAD=success")

    youtube.captions().insert(
        part="snippet",
        body={"snippet": {
            "videoId": video_id,
            "language": "en",
            "name": "English",
            "isDraft": False,
        }},
        media_body=MediaFileUpload(str(captions[0]), mimetype="application/octet-stream"),
    ).execute()
    print("CAPTIONS_UPLOAD=success")
    print("PRIVACY_STATUS=private")


if __name__ == "__main__":
    main()

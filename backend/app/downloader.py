from __future__ import annotations

from pathlib import Path
import yt_dlp

class DownloadError(RuntimeError):
    pass

def download_source(url: str, destination: Path) -> Path:
    if not url.startswith(("http://", "https://")):
        raise DownloadError("Source URL must use http:// or https://")
    destination.mkdir(parents=True, exist_ok=True)
    options = {
        "outtmpl": str(destination / "source.%(ext)s"),
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "retries": 3,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=True)
            filename = Path(downloader.prepare_filename(info))
            candidates = list(destination.glob("source.*"))
            if candidates:
                return candidates[0]
            return filename
    except Exception as exc:
        raise DownloadError(f"Source download failed: {exc}") from exc

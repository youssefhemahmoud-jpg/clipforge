from __future__ import annotations
import json
import subprocess
from pathlib import Path
from typing import Any

class MediaProbeError(RuntimeError):
    pass

def probe_media(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise MediaProbeError(f"Media file does not exist: {path}")
    command = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)
    except FileNotFoundError as exc:
        raise MediaProbeError("ffprobe is not installed or is not on PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise MediaProbeError(exc.stderr.strip() or "ffprobe failed") from exc
    except subprocess.TimeoutExpired as exc:
        raise MediaProbeError("ffprobe timed out") from exc
    except json.JSONDecodeError as exc:
        raise MediaProbeError("ffprobe returned invalid JSON") from exc

def media_summary(probe: dict[str, Any]) -> dict[str, Any]:
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {"duration_seconds": float(probe.get("format", {}).get("duration", 0) or 0), "has_video": video is not None, "has_audio": audio is not None, "width": video.get("width") if video else None, "height": video.get("height") if video else None, "fps": video.get("r_frame_rate") if video else None, "video_codec": video.get("codec_name") if video else None, "audio_codec": audio.get("codec_name") if audio else None}

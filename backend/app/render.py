from __future__ import annotations
import subprocess
from pathlib import Path
from .media import MediaProbeError, probe_media

class RenderError(RuntimeError):
    pass

def render_vertical_clip(source: Path, output: Path, start: float, duration: float) -> dict:
    if start < 0 or duration <= 0:
        raise RenderError("start must be non-negative and duration must be positive")
    output.parent.mkdir(parents=True, exist_ok=True)
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    command = ["ffmpeg", "-hide_banner", "-y", "-ss", f"{start:.3f}", "-i", str(source), "-t", f"{duration:.3f}", "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(output)]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=180)
    except FileNotFoundError as exc:
        raise RenderError("ffmpeg is not installed or is not on PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise RenderError(exc.stderr.strip()[-2000:] or "ffmpeg failed") from exc
    except subprocess.TimeoutExpired as exc:
        raise RenderError("ffmpeg render timed out") from exc
    if not output.is_file() or output.stat().st_size == 0:
        raise RenderError("ffmpeg produced no output")
    try:
        return {"output": str(output), "media": probe_media(output)}
    except MediaProbeError as exc:
        raise RenderError(f"render validation failed: {exc}") from exc

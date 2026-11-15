from pathlib import Path
import pytest
from app.media import MediaProbeError, media_summary, probe_media

def test_media_summary_handles_video_and_audio():
    result = media_summary({"format": {"duration": "12.5"}, "streams": [{"codec_type": "video", "width": 1920, "height": 1080, "r_frame_rate": "30/1", "codec_name": "h264"}, {"codec_type": "audio", "codec_name": "aac"}]})
    assert result["duration_seconds"] == 12.5
    assert result["has_audio"] is True
    assert result["width"] == 1920

def test_probe_rejects_missing_file(tmp_path: Path):
    with pytest.raises(MediaProbeError):
        probe_media(tmp_path / "missing.mp4")

from app.discovery import build_windows
from app.transcription_adapter import Word

def test_build_windows_creates_target_length_windows():
    words = [Word(f"w{i}", float(i * 2), float(i * 2 + 1)) for i in range(60)]
    windows = build_windows(words, min_seconds=60, max_seconds=90, stride=15)
    assert windows
    assert all(window.end - window.start >= 60 for window in windows)
    assert all(window.text for window in windows)

def test_build_windows_rejects_invalid_ranges():
    words = [Word("hello", 0, 1)]
    assert build_windows(words, min_seconds=90, max_seconds=60) == []

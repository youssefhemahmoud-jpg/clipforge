from __future__ import annotations
from dataclasses import dataclass
from .transcription import Word, text_between

@dataclass(frozen=True)
class TranscriptWindow:
    start: float
    end: float
    text: str
    has_start: bool
    has_end: bool

def build_windows(words: list[Word], min_seconds: float = 60, max_seconds: float = 90, stride: float = 15) -> list[TranscriptWindow]:
    if not words or min_seconds <= 0 or max_seconds < min_seconds:
        return []
    last = words[-1].end
    windows = []
    start = max(0.0, words[0].start)
    while start < last:
        target_end = min(start + max_seconds, last)
        available = target_end - start
        if available >= min_seconds:
            end = min(target_end, start + max(min_seconds, available))
            text = text_between(words, start, end)
            if text:
                windows.append(TranscriptWindow(start, end, text, bool(text), bool(text)))
        start += stride
    return windows

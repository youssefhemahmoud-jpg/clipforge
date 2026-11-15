from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Word:
    text: str
    start: float
    end: float
    confidence: float = 1.0

class TranscriptionError(RuntimeError):
    pass

def transcribe(path: Path, model_size: str = "small") -> list[Word]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise TranscriptionError("faster-whisper is not installed") from exc
    if not path.is_file():
        raise TranscriptionError(f"Audio source does not exist: {path}")
    try:
        model = WhisperModel(model_size, device="auto", compute_type="auto")
        segments, _ = model.transcribe(str(path), word_timestamps=True, vad_filter=True)
        words = []
        for segment in segments:
            for item in segment.words or []:
                words.append(Word(item.word.strip(), float(item.start), float(item.end), float(item.probability)))
        return words
    except Exception as exc:
        raise TranscriptionError(f"Transcription failed: {exc}") from exc

def text_between(words: list[Word], start: float, end: float) -> str:
    return " ".join(word.text for word in words if word.end > start and word.start < end).strip()

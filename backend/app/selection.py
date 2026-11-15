from dataclasses import dataclass

@dataclass(frozen=True)
class Candidate:
    start: float
    end: float
    hook: float
    payoff: float
    value: float
    emotion: float
    flow: float
    prompt_fit: float = 0.0
    audience: float = 0.0
    visual: float = 0.0

    @property
    def duration(self) -> float:
        return self.end - self.start

    @property
    def score(self) -> float:
        if self.duration < 15:
            return 0.0
        weighted = (self.hook * .18 + self.payoff * .14 + self.value * .14 +
                    self.emotion * .12 + self.flow * .12 + self.prompt_fit * .10 +
                    self.audience * .08 + self.visual * .07)
        duration_bonus = 1.0 if 60 <= self.duration <= 90 else .85
        return round(max(0.0, min(99.0, weighted * duration_bonus)), 2)

def overlaps(a: Candidate, b: Candidate) -> bool:
    return max(a.start, b.start) < min(a.end, b.end)

def select_non_overlapping(candidates: list[Candidate], limit: int) -> list[Candidate]:
    selected = []
    for candidate in sorted(candidates, key=lambda item: item.score, reverse=True):
        if all(not overlaps(candidate, current) for current in selected):
            selected.append(candidate)
        if len(selected) >= limit:
            break
    return selected

from app.selection import Candidate, select_non_overlapping

def c(start, end, score):
    return Candidate(start, end, score, score, score, score, score, score, score, score)

def test_short_candidates_are_not_viable():
    assert c(0, 10, 99).score == 0

def test_selection_is_score_ordered_and_non_overlapping():
    chosen = select_non_overlapping([c(0, 70, 70), c(60, 130, 99), c(150, 220, 80)], 2)
    assert [(item.start, item.end) for item in chosen] == [(60, 130), (150, 220)]

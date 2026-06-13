import string
import syllables

def get_syllable_count_for_line(line: str) -> int:
    """Estimates the syllable count for a given line of text by stripping punctuation."""
    clean_line = line.translate(str.maketrans('', '', string.punctuation))
    return sum(syllables.estimate(word) for word in clean_line.split())

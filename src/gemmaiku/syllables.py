import string
import pronouncing

def _fallback_syllable_count(word: str) -> int:
    """Estimates the syllable count of a word using a heuristic ruleset based on vowels."""
    word = word.lower()
    word = "".join(char for char in word if char.isalpha())
    if not word:
        return 0
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1
    return max(1, count)

def get_syllable_count_for_line(line: str) -> int:
    """Estimates the syllable count for a given line of text using CMUDict lookup and a rule-based fallback."""
    clean_line = line.translate(str.maketrans('', '', string.punctuation))
    total_syllables = 0
    for word in clean_line.split():
        word_clean = word.lower()
        phones = pronouncing.phones_for_word(word_clean)
        if phones:
            total_syllables += pronouncing.syllable_count(phones[0])
        else:
            total_syllables += _fallback_syllable_count(word_clean)
    return total_syllables


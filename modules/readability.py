from nltk.tokenize import sent_tokenize, word_tokenize


def _count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def get_readability(text: str) -> dict:
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]

    if not sentences or not words:
        return {"score": 0.0, "grade": "N/A"}

    syllable_count = sum(_count_syllables(w) for w in words)
    score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllable_count / len(words))
    score = round(score, 1)

    if score >= 90:
        grade = "Very Easy"
    elif score >= 70:
        grade = "Easy"
    elif score >= 50:
        grade = "Moderate"
    elif score >= 30:
        grade = "Difficult"
    else:
        grade = "Very Difficult"

    return {"score": score, "grade": grade}


import re
import string
from collections import Counter


# 1. STRING MANIPULATION

def clean_text(text: str) -> str:
    """Lowercase and strip extra whitespace from the text."""
    return text.lower().strip()


def count_characters(text: str) -> dict:
    """
    Count total characters, letters, digits, spaces, punctuation.
    Uses: Strings, Dictionary
    """
    stats = {
        "total_chars":   len(text),
        "letters":       sum(1 for c in text if c.isalpha()),
        "digits":        sum(1 for c in text if c.isdigit()),
        "spaces":        text.count(" "),
        "punctuation":   sum(1 for c in text if c in string.punctuation),
    }
    return stats


def count_sentences(text: str) -> int:
    """Count sentences using regex (splits on . ! ?)."""
    sentences = re.split(r'[.!?]+', text.strip())
    return len([s for s in sentences if s.strip()])


def count_paragraphs(text: str) -> int:
    """Count paragraphs separated by blank lines."""
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return len([p for p in paragraphs if p.strip()])


# 2. DICTIONARIES — Word Frequency

def get_word_frequency(text: str, top_n: int = 10) -> dict:
    """
    Returns the top N most frequent words.
    Uses: Dictionary, String Manipulation, Regex
    """
    # Remove punctuation using regex, split into words
    words = re.findall(r'\b[a-z]+\b', text.lower())
    freq = Counter(words)                  # Counter is a dict subclass
    return dict(freq.most_common(top_n))


def average_word_length(text: str) -> float:
    """Calculate the average word length."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    return round(sum(len(w) for w in words) / len(words), 2)


# 3. SETS — Unique Words & Stop Words

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "it", "its", "be",
    "was", "are", "were", "this", "that", "i", "you", "he", "she",
    "we", "they", "not", "as", "if", "so", "do", "does", "did",
    "have", "has", "had", "will", "would", "can", "could", "should",
    "my", "your", "his", "her", "our", "their", "what", "which",
    "who", "whom", "when", "where", "why", "how", "all", "been",
    "than", "then", "no", "up", "about", "into", "than", "such",
    "more", "also", "just", "very", "much", "any", "there",
}


def unique_words(text: str) -> set:
    """Return a set of all unique words (lowercased)."""
    return set(re.findall(r'\b[a-z]+\b', text.lower()))


def meaningful_words(text: str) -> set:
    """
    Return unique words excluding common stop words.
    Uses: Sets (set difference)
    """
    return unique_words(text) - STOP_WORDS


def vocabulary_richness(text: str) -> float:
    """
    Type-Token Ratio: unique words / total words.
    Higher = richer vocabulary (0.0 – 1.0)
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 3)


# 4. REGULAR EXPRESSIONS

def find_emails(text: str) -> list:
    """Extract all email addresses using regex."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def find_urls(text: str) -> list:
    """Extract all URLs using regex."""
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text)


def find_hashtags(text: str) -> list:
    """Extract hashtags (e.g. #python)."""
    return re.findall(r'#\w+', text)


def find_mentions(text: str) -> list:
    """Extract @mentions."""
    return re.findall(r'@\w+', text)


def find_numbers(text: str) -> list:
    """Extract all numbers (integers and decimals)."""
    return re.findall(r'\b\d+(?:\.\d+)?\b', text)


def find_capitalized_words(text: str) -> list:
    """Find proper nouns / capitalized words (not sentence starts)."""
    return re.findall(r'(?<=[.!?\s])[A-Z][a-z]+', text)


# 5. READABILITY

def flesch_reading_ease(text: str) -> float:
    """
    Approximates Flesch Reading Ease score.
    90–100: Very Easy | 60–70: Standard | 0–30: Very Difficult
    """
    words = re.findall(r'\b\w+\b', text)
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s for s in sentences if s.strip()]

    if not words or not sentences:
        return 0.0

    # Rough syllable count: each vowel group = 1 syllable
    def count_syllables(word):
        word = word.lower()
        vowels = re.findall(r'[aeiou]+', word)
        return max(1, len(vowels))

    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_len = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)

    score = 206.835 - (1.015 * avg_sentence_len) - (84.6 * avg_syllables_per_word)
    return round(max(0, min(100, score)), 1)


def reading_time(text: str, wpm: int = 200) -> str:
    """Estimate reading time (average adult reads ~200 wpm)."""
    words = re.findall(r'\b\w+\b', text)
    minutes = len(words) / wpm
    if minutes < 1:
        return f"~{int(minutes * 60)} seconds"
    return f"~{minutes:.1f} minutes"


# 6. MAIN ANALYZER  (ties everything together)

def analyze(text: str, top_n: int = 10) -> dict:
    """
    Run the full analysis pipeline and return a results dictionary.
    """
    words = re.findall(r'\b[a-z]+\b', text.lower())
    word_count = len(words)

    results = {
        # ── Basic Stats ──────────────────────────────
        "word_count":           word_count,
        "sentence_count":       count_sentences(text),
        "paragraph_count":      count_paragraphs(text),
        "char_stats":           count_characters(text),
        "avg_word_length":      average_word_length(text),

        # ── Vocabulary (Sets) ────────────────────────
        "unique_word_count":    len(unique_words(text)),
        "meaningful_word_count":len(meaningful_words(text)),
        "vocabulary_richness":  vocabulary_richness(text),

        # ── Frequency (Dictionaries) ─────────────────
        "top_words":            get_word_frequency(text, top_n),

        # ── Regex Extractions ────────────────────────
        "emails":               find_emails(text),
        "urls":                 find_urls(text),
        "hashtags":             find_hashtags(text),
        "mentions":             find_mentions(text),
        "numbers":              find_numbers(text),
        "capitalized_words":    find_capitalized_words(text),

        # ── Readability ──────────────────────────────
        "flesch_score":         flesch_reading_ease(text),
        "reading_time":         reading_time(text),
    }
    return results


def print_report(text: str):
    """Pretty-print the full analysis report."""
    r = analyze(text)

    sep = "─" * 50

    print(f"\n{'═' * 50}")
    print("  TEXT ANALYZER REPORT")
    print(f"{'═' * 50}\n")

    print("📊  BASIC STATISTICS")
    print(sep)
    print(f"  Words          : {r['word_count']}")
    print(f"  Sentences      : {r['sentence_count']}")
    print(f"  Paragraphs     : {r['paragraph_count']}")
    print(f"  Total chars    : {r['char_stats']['total_chars']}")
    print(f"  Letters        : {r['char_stats']['letters']}")
    print(f"  Digits         : {r['char_stats']['digits']}")
    print(f"  Spaces         : {r['char_stats']['spaces']}")
    print(f"  Avg word length: {r['avg_word_length']} chars")

    print(f"\n📚  VOCABULARY  (using Sets)")
    print(sep)
    print(f"  Unique words   : {r['unique_word_count']}")
    print(f"  Meaningful words (stop-words removed): {r['meaningful_word_count']}")
    print(f"  Vocabulary richness (TTR): {r['vocabulary_richness']}")

    print(f"\n🔤  TOP WORDS  (using Dictionaries)")
    print(sep)
    for word, count in r['top_words'].items():
        bar = "█" * count
        print(f"  {word:<15} {count:>3}  {bar}")

    print(f"\n🔍  REGEX EXTRACTIONS")
    print(sep)
    print(f"  Emails    : {r['emails'] or 'none'}")
    print(f"  URLs      : {r['urls'] or 'none'}")
    print(f"  Hashtags  : {r['hashtags'] or 'none'}")
    print(f"  Mentions  : {r['mentions'] or 'none'}")
    print(f"  Numbers   : {r['numbers'] or 'none'}")
    print(f"  Proper nouns (capitalized): {r['capitalized_words'][:8] or 'none'}")

    print(f"\n📖  READABILITY")
    print(sep)
    score = r['flesch_score']
    if score >= 80:    level = "Very Easy"
    elif score >= 60:  level = "Standard"
    elif score >= 40:  level = "Difficult"
    else:              level = "Very Difficult"
    print(f"  Flesch Reading Ease: {score}  ({level})")
    print(f"  Estimated reading time: {r['reading_time']}")

    print(f"\n{'═' * 50}\n")

SAMPLE_TEXT = input("Enter the text to analyze: ")

if __name__ == "__main__":
    print_report(SAMPLE_TEXT)
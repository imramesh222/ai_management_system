from typing import List
import string

def most_frequent_vowel_and_consonant(s: str) -> List[str]:
    s = s.lower()
    vowels = 'aeiou'
    freq_vowel = {}
    freq_consonant = {}
    for ch in s:
        if ch in string.ascii_lowercase:
            if ch in vowels:
                freq_vowel[ch] = freq_vowel.get(ch, 0) + 1
            else:
                freq_consonant[ch] = freq_consonant.get(ch, 0) + 1
    # Find most frequent vowel
    most_vowel = min(
        (k for k, v in freq_vowel.items() if v == max(freq_vowel.values(), default=0)),
        default='',
    ) if freq_vowel else ''
    # Find most frequent consonant
    most_consonant = min(
        (k for k, v in freq_consonant.items() if v == max(freq_consonant.values(), default=0)),
        default='',
    ) if freq_consonant else ''
    return [most_vowel, most_consonant]
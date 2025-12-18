from typing import List

def get_word_length(word: str) -> int:
    return len(word)

def sort_words(words: List[str]) -> List[str]:
    words.sort(key=get_word_length, reverse = True)
    return words

def get_abs(word: str) -> int:
    return abs(word)

def sort_numbers(numbers: List[int]) -> List[int]:
    numbers.sort(key=get_abs)
    return numbers

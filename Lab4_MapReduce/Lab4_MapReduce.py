# Maria Estrada - Due Sunday Sep 22, 2024

from collections import defaultdict
import re
from functools import reduce

# Function to read words from the file
def read_words_from_file(filename):
    """Reads words from a file, removes punctuation, and returns a list of words."""
    with open(filename, 'r') as file:
        text = file.read().lower()  # Convert to lowercase for case-insensitive counting

        # Remove punctuation using regular expressions
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()

# Count the number of words
def map_words_to_count(words):
    return list(map(lambda word: (word, 1), words))

# Combine each word using defaultdict
def add_word_counts(mapped_words):
    word_count = defaultdict(int)
    
    # Update word count
    def update_WC(accumulator, word_count_pair):
        word, count = word_count_pair
        accumulator[word] += count 
        return accumulator
    
    # Accumulate counts
    return reduce(update_WC, mapped_words, word_count)

filename = '/workspaces/CS3210_PPL/Lab4_MapReduce/words.txt'

words = read_words_from_file(filename)

mapped_words = map_words_to_count(words)

word_count = add_word_counts(mapped_words)

# Print 
for word, count in word_count.items():
    print(f"'{word}': {count}")

'''
'hello': 1
'cs3210': 1
'this': 2
'lab': 2
'will': 2
'help': 2
'you': 2
'to': 2
'learn': 2
'map': 2
'and': 2
'reduce': 2
'i': 1
'repeat': 1
'''
# Maria Estrada - Due Sunday Sep 22, 2024

#Convert the given code using maps and reduce to simulate the MapReduce algorithm. MapReduce is the main batch processing framework from the Apache Hadoop project. Google developed it and published an article describing the concept in 2004.

from collections import defaultdict
import re

def read_words_from_file(filename):
    """Reads words from a file, removes punctuation, and returns a list of words."""
    with open(filename, 'r') as file:
        text = file.read().lower()  # Convert to lowercase for case-insensitive counting

        # Remove punctuation using regular expressions
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()

def count_word_occurrences(words):
    """Counts occurrences of each word using a dictionary."""
    word_count = defaultdict(int)  # Dictionary to store word counts
    # Loop through each word and update its count

    for word in words:
        word_count[word] += 1

    return word_count

# Using Functions

filename = 'c:\\Users\\rranjidh\\Documents\words.txt'  # Replace with the path to your file

words = read_words_from_file(filename)

word_count = count_word_occurrences(words)

# Print the word counts
for word, count in word_count.items():
    print(f"'{word}': {count}")
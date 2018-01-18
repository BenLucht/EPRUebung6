"""
Text module, implements a text clas for storing text and statistics on the text.
"""

__author__ = "xxxxxxx: Ben, xxxxxxx: Anne"
__copyright__ = "Copyright 2017/2018 – EPR-Goethe-Uni"
__credits__ = "We would like to thank our coffee for the morning motivation."
__email__ = "xxxxxxxx@stud.uni-frankfurt.de, xxxxxxxx@stud.uni-frankfurt.de"

import string
import itertools
import re
import json

class text():
    def __init__(self, path):
        """
        Reads text from a file, stores it and text statistics such as:
        word_count : amount of full words in the text (excl. apostrophed additions)
        keystroke_count : total amount of keystrokes needed to produce the text
        character_count : amount of characters in the text (excl. spaces)
        character_distribution : frequency distribution of characters in the text
        word_distribution : frequency distribution of words in the text
        average_word_length : average length of the words in the text
        """

        #list of common encodings to try
        codec_list = itertools.chain(['utf-32', 'utf-16', 'utf-8', 'ascii', 'latin-1'])

        #tries reading file with different encodings, saving first match
        while True:
            try:
                self.decoded_as = next(codec_list)
                with open(path, 'r', encoding=self.decoded_as, errors='strict') as text:
                    self.content = text.read()
                    break
            except:
                pass

        self.word_count = self.count_words(self.content)
        self.keystroke_count = self.count_keystrokes(self.content)
        self.character_count = self.count_characters(self.content)
        self.character_distribution = self.distribution_characters()
        self.word_distribution = self.distribution_words()
        self.average_word_length = self.average_words()

    def count_words(self, content):
        """Counts the words in the given text, excluding 'apostrophed' abbreviations."""

        #standard punctuation plus extra characters
        punctuation = string.punctuation + '´’'
        #translation table for removing punctuation from the text
        trans_table = str.maketrans(dict(zip(punctuation, ['' for ch in punctuation])))
        #regex to find all words (1+ characters) in the text
        words = re.compile(r'\b\w+\b')

        #remove puntuation from text
        content = content.translate(trans_table)

        return len(words.findall(content))

    def count_keystrokes(self, content):
        """
        Counts the simple amount of keystrokes
        (does not account for shift+char to make capital letters)
        """
        chars = re.compile(r'(\w|\W)')

        #add double count for capitals
        #caps = re.compile(r'[A-Z]')

        return len(chars.findall(content)) # + len(caps.findall(content))

    def count_characters(self, content):
        """Counts all characters excl. spaces."""

        #everything but whitespace of any kind
        chars = re.compile(r'\S')

        return len(chars.findall(content))

    def distribution_characters(self, print_result=False):
        test = [(item, self.content.count(item)*1.0/self.keystroke_count) \
                for item in set(self.content)]

        return sorted(test, key=lambda t: t[1])[::-1]

    def distribution_words(self):
        return None

    def print_distribution(self):
        output = ''
        for item in self.character_distribution:
            if item[0] == '\n':
                character = r'\n'
            elif item[0] == '\t':
                character == r'\t'
            elif item[0] == ' ':
                character = '" "'
            else:
                character = item[0]

            output += '{:^5}| {:6.2f}% \n'.format(character, item[1]*100)

        print(output)

    def average_words(self):
        return None

    def save_json(self, file_name):
        output = {
            "content": self.content,
            "word_count": self.word_count,
            "keystroke_count": self.keystroke_count,
            "character_count": self.character_count,
            "character_distribution": self.character_distribution,
            "word_distribution": self.word_distribution,
            "average_word_length": self.average_word_length
        }

        try:
            if '.' in file_name:
                if '.txt'in file_name or '.json' in file_name:
                    pass
                else:
                    raise ValueError('file_name problem: file name must be .txt, ' + \
                                     '.json or neither (will then be saved as .json)')
            else:
                file_name = file_name + '.json'

            with open(file_name, 'w') as file:
                json.dump(output, file)

        except ValueError as e:
            print('ValueError:', e)

if __name__ == '__main__':
    pass
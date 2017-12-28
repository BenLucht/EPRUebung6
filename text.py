import string
import itertools

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

        self.word_count = self.count_words()
        self.keystroke_count = self.count_keystrokes()
        self.character_count = self.count_characters()
        self.character_distribution = self.distribution_characters()
        self.word_distribution = self.distribution_words()
        self.average_word_length = self.average_words()

    def count_words(self):
        pass

    def count_keystrokes(self):
        pass

    def count_characters(self):
        pass

    def distribution_characters(self):
        pass

    def distribution_words(self):
        pass

    def average_words(self):
        pass
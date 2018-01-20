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
import os
import time

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
        test = [(item, self.content.count(item)) \
                for item in set(self.content)]

        return sorted(test, key=lambda t: t[1])[::-1]

    def distribution_words(self):
        return None

    def print_distribution(self, percentage=False):
        output = ''
        for item in self.character_distribution:
            if item[0] == '\n':
                character = r'\n'
            elif item[0] == '\t':
                character == r'\t'
            elif item[0] == ' ':
                character = '<space>'
            else:
                character = item[0]

            if percentage:
                output += '{:^9}| {:6.2f}%\n'.format(character, item[1]*1.0/self.keystroke_count*100)
            else:
                output += '{:^9}| {}\n'.format(character, item[1])

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

    def show_stats(self):
        print("content: {:20} ...".format(self.content))
        print("word_count:", self.word_count)
        print("keystroke_count:", self.keystroke_count)
        print("character_count:", self.character_count)
        print("character_distribution: {}..".format(self.character_distribution[0]))
        print("word_distribution:", self.word_distribution)
        print("average_word_length:", self.average_word_length)

class commandline_interface():
    """Class to handle a command line interface for the text class."""

    def __init__(self):
        """Initializes by calling the main command line dialog."""
        self.textfile = None

        self.dialog()

    def cls(self):
        """Clears the command line to avoid clutter."""
        os.system('cls' if os.name=='nt' else 'clear')

    def dialog(self):
        """Main command line dialog."""
        self.cls()
        print('---------------------------------------------------------')
        print('Enter "open" to ggo to open file dialog\n' + \
              'Enter "save" to go to save file dialog\n' + \
              'Enter "exit" to exit')
        print('---------------------------------------------------------')

        action = input()

        #choice of action depending on user input
        if action == 'open':
            self.open_file(os.getcwd())
        elif action == 'exit':
            #exits the program
            os._exit(0)
        elif action == 'save':
            #uses text method to save file isf a file was loaded
            if self.textfile is not None:
                self.save_file(os.getcwd())
            else:
                print('Please load a file first! (wait a sec)')
                time.sleep(2)
                self.dialog()

    def ls(self, directory):
        """Implements a convenient view of the current directory."""

        #list of directories in the current directory
        subfolders = [f.name for f in os.scandir(directory) if f.is_dir()]
        #list of files in the current directory
        subfiles = [f.name for f in os.scandir(directory) if f.is_file()]

        #loop through both lists to print folder contents
        print('{:20} {:20} \n'.format('Folders', 'Files'))
        for folder, file in list(itertools.zip_longest(subfolders, subfiles)):
            if folder is None:
                folder = ''
            elif file is None:
                file = ''

            print('{:20} {:20}'.format(folder, file))

        return (subfolders, subfiles)

    def open_file(self, original_directory):
        """Open file dialog similar to tkinter."""
        current_directory = original_directory

        while True:
            self.cls()
            print('---------------------------------------------------------')
            print('Enter "up" to get to parent directory\n' + \
                  'Enter <folder name> to go to that directory\n' + \
                  'Enter "backhome" to return to origin directory\n' + \
                  'Enter "root" to go to highest level directory possible\n' + \
                  'Enter "open: " + file name to load a file\n' + \
                  'Enter "exit" to exit file open dialog\n')

            path = current_directory
            print('You are currently at ' + path + '\n')

            subfolders, subfiles = self.ls(path)
            print('---------------------------------------------------------')

            action = input('Please enter your command:')

            #choice of action depending on user input
            if action in subfolders:
                #changes current directory to the selected one
                os.chdir(action)
            elif action == 'up':
                #changes to parent directory
                os.chdir('..')
            elif action[:5] == 'open:':
                #loads text file from path and shows stats
                print('Opening file: ' + path + '/' + action[6:])
                self.textfile = text(path + '/' + action[6:])
                self.textfile.show_stats()
                input('Press <Enter> to go back to main dialog.')
                self.dialog()
                break
            elif action == 'exit':
                #back to main dialog
                self.dialog()
            elif action == 'backhome':
                #back to the original directory
                os.chdir(original_directory)
            elif action == 'root':
                #goes to the file system root
                temp = original_directory.split('/')
                os.chdir(temp[0] + '/')

            current_directory = os.getcwd()

        #change working directory back to where one started
        os.chdir(original_directory)

    def save_file(self, original_directory):
        """Save file dialog similar to tkinter."""
        current_directory = original_directory

        while True:
            self.cls()
            print('---------------------------------------------------------')
            print('Enter "up" to get to parent directory\n' + \
                  'Enter <folder name> to go to that directory\n' + \
                  'Enter "backhome" to return to origin directory\n' + \
                  'Enter "root" to go to highest level directory possible\n' + \
                  'Enter "save:" + file name to load a file\n' + \
                  'Enter "exit" to exit file save dialog\n')

            path = current_directory
            print('You are currently at ' + path + '\n')

            subfolders, subfiles = self.ls(path)
            print('---------------------------------------------------------')

            action = input('Please enter your command:')

            if action in subfolders:
                #changes current directory to the selected one
                os.chdir(action)
            elif action == 'up':
                #changes to parent directory
                os.chdir('..')
            elif action[:5] == 'save:':
                #uses text class save_json method to save file
                print('Saving file to: ' + path + '/' + action[6:])
                self.textfile.save_json(path + '/' + action[6:])
                self.dialog()
                break
            elif action == 'exit':
                #back to main dialog
                self.dialog()
            elif action == 'backhome':
                #back to the original directory
                os.chdir(original_directory)
            elif action == 'root':
                #goes to the file system root
                temp = original_directory.split('/')
                os.chdir(temp[0] + '/')

            current_directory = os.getcwd()

        os.chdir(original_directory)

if __name__ == '__main__':
    pass
"""
Tkinter module to implement the GUI for text statistics.
"""

__author__ = "xxxxxxx: Ben, xxxxxxx: Anne"
__copyright__ = "Copyright 2017/2018 – EPR-Goethe-Uni"
__credits__ = "We would like to thank our coffee for the morning motivation."
__email__ = "xxxxxxxx@stud.uni-frankfurt.de, xxxxxxxx@stud.uni-frankfurt.de"

import tkinter as tk
from tkinter import filedialog
import os
from text import text

class text_stat_window():
    """Class that contains all methods needed for the stats window."""

    def open_callback(self):
        """Method for file open dialog, text processing, and display of statistics."""

        #file open dialog (opens at current directory, allows only text files)
        path =  filedialog.askopenfilename( \
            initialdir=os.getcwd(), \
            title="Select file", \
            filetypes=(("text files","*.txt"),("text files","*.json"),("all files","*.*")) \
        )

        try:
            #check if dialog closed by 'cancel'
            if path == '':
                return
            else:
                #instantiate text object from path
                self.txt = text(path)
                #get file name, not entire path
                filename = path.split('/')[-1]
                #list of variables to be displayed in gui
                txt_vars = [filename, \
                            self.txt.word_count, \
                            self.txt.keystroke_count, \
                            self.txt.character_count, \
                            #self.txt.character_distribution, \
                            #self.txt.word_distribution, \
                            self.txt.average_word_length]
                gridrow = 1 #counting rows in grid

                #make a new label for each of the text statistics
                for item in txt_vars:
                    lbl = tk.Label(self.root, text=item)
                    lbl.grid(column=1, row=gridrow)
                    gridrow += 1

                self.root.update() #redraw gui with new labels

        except:
            return

    def save_callback(self):
        #file save dialog
        path =  filedialog.asksaveasfilename(initialdir=os.getcwd())
        try:
            #check if dialog closed by 'cancel'
            if path == '':
                return
            else:
                #save statistics at path via text object method
                self.txt.save_json(path)
        except:
            print('Could not save file.')

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Text Stat Window')
        self.txt = None

        #-----make buttons to open and save file-------------------------------------
        btn_load = tk.Button(self.root, text='Open File', command=self.open_callback)
        btn_load.grid(row=0, column=0, columnspan=5)

        btn_save = tk.Button(self.root, text='Save Stats', command=self.save_callback)
        btn_save.grid(row=10, column=0, columnspan=5)

        #-----make labels to describe statistics-------------------------------------
        lbl_name = tk.Label(self.root, text='file name:')
        lbl_name.grid(row=1, column=0)

        lbl_word_count = tk.Label(self.root, text='word count:')
        lbl_word_count.grid(row=2, column=0)

        lbl_keystroke_count = tk.Label(self.root, text='keystroke count:')
        lbl_keystroke_count.grid(row=3, column=0)

        lbl_character_count = tk.Label(self.root, text='character count:')
        lbl_character_count.grid(row=4, column=0)

        lbl_average_word_length = tk.Label(self.root, text='average word length:')
        lbl_average_word_length.grid(row=5, column=0)


        tk.mainloop()

if __name__ == '__main__':
    text_stat_window()
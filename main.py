"""
Main Module for EPR6 exercises.
"""

from text import text
from text_statistics_interface import text_stat_window

__author__ = "xxxxxxx: Ben, xxxxxxx: Anne"
__copyright__ = "Copyright 2017/2018 – EPR-Goethe-Uni"
__credits__ = "We would like to thank our coffee for the morning motivation."
__email__ = "xxxxxxxx@stud.uni-frankfurt.de, xxxxxxxx@stud.uni-frankfurt.de"

if __name__ == '__main__':
    morgen_kinder = text('src/Morgen_Kinder.txt')

    #text_stat_window() #opens the tkinter interface
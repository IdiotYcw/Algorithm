#!/usr/bin/env python
import argparse
import sys
import codecs

if sys.version_info[0] == 2:
    from itertools import izip
else:
    izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
    if type(fh) is str:
        fh = open(fh, code)
    ret = gzip.open(fh.name, code if code.endswith("t") else code + "t") if fh.name.endswith(".gz") else fh
    if sys.version_info[0] == 2:
        if code.startswith('r'):
            ret = reader(fh)
        elif code.startswith('w'):
            ret = writer(fh)
        else:
            sys.stderr.write("I didn't understand code " + code + "\n")
            sys.exit(1)
    return ret


def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
    ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
    group = parser.add_mutually_exclusive_group()
    dest = arg if dest is None else dest
    group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
    group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


class LimerickDetector:
    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def apostrophe_tokenize(self, text):
        """
        for python 3
        :param text:
        :return:
        """
        table = str.maketrans({k: None for k in punctuation.replace("'", "")})
        text = text.translate(table)
        lines = text.strip().split('\n')
        lines = list(map(lambda l: l.strip(), lines))
        lines = list(filter(lambda x: len(x) > 0, lines))

        return lines

    def guess_syllables(self, word):
        """
        not reasonable at all o_O
        """
        vowel = 'aeiou'
        return sum(word.count(c) for c in vowel)

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        word = word.strip().lower()
        shorter_pronounce = min(self._pronunciations.get(word, [[]]), key=len)

        # len(list(filter(lambda p: p[-1].isdigit(), short_pronounce)))
        return list(map(lambda p: p[-1].isdigit(), shorter_pronounce)).count(True) \
            if shorter_pronounce else 1

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        def sounds_after_first_consonant(sound_list):
            for index, sound in enumerate(sound_list):
                if not sound[-1].isdigit() and index != len(sound_list) - 1:
                    return ''.join(sound_list[index+1:])
            return ''.join(sound_list)

        for a_sound_list in self._pronunciations.get(a, [[]]):
            for b_sound_list in self._pronunciations.get(b, [[]]):
                if not a_sound_list or not b_sound_list:
                    return False

                if len(a_sound_list) == len(b_sound_list) and \
                        sounds_after_first_consonant(a_sound_list) == sounds_after_first_consonant(b_sound_list):
                    return True
                if len(a_sound_list) < len(b_sound_list) and \
                        ''.join(b_sound_list).endswith(sounds_after_first_consonant(a_sound_list)):
                    return True
                if len(a_sound_list) > len(b_sound_list) and \
                        ''.join(a_sound_list).endswith(sounds_after_first_consonant(b_sound_list)):
                    return True

        return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """

        lines = self.apostrophe_tokenize(text)
        if len(lines) != 5:
            return False

        def lines_rhymes(line1, line2):
            return self.rhymes(line1.split(' ')[-1], line2.split(' ')[-1])

        # line1 rhymes line2, line2 rhymes line3 !-> line1 rhymes line3
        if not all([
            lines_rhymes(lines[0], lines[1]),
            lines_rhymes(lines[0], lines[4]),
            lines_rhymes(lines[1], lines[4]),
            lines_rhymes(lines[2], lines[3]),
        ]):
            return False

        if any([
            lines_rhymes(lines[0], lines[2]),
            lines_rhymes(lines[0], lines[3]),
            lines_rhymes(lines[1], lines[2]),
            lines_rhymes(lines[1], lines[3]),
            lines_rhymes(lines[4], lines[2]),
            lines_rhymes(lines[4], lines[3]),
        ]):
            return False

        # additional
        lines_num_syllables = []
        for index, line in enumerate(lines):
            word_list = line.strip().split(' ')
            word_list = list(filter(lambda x: len(x) > 0, word_list))
            lines_num_syllables.append(
                sum(list(map(self.num_syllables, word_list)))
            )

        lns = lines_num_syllables
        if min(lns) < 4:
            return False
        if max(lns[2], lns[3]) >= min(lns[0], lns[1], lns[4]):
            return False
        if max(lns[0], lns[1], lns[4]) - min(lns[0], lns[1], lns[4]) > 2:
            return False
        if max(lns[2], lns[3]) - min(lns[2], lns[3]) > 2:
            return False

        return True


# The code below should not need to be modified
def main():
    parser = argparse.ArgumentParser(
        description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help="output file")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    infile = prepfile(args.infile, 'r')
    outfile = prepfile(args.outfile, 'w')

    ld = LimerickDetector()
    lines = ''.join(infile.readlines())
    outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))


if __name__ == '__main__':
    main()

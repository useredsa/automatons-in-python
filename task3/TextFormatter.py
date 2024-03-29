#!/usr/bin/python3
import regex as re
import sys

class SpanishFormatter(object):
    '''Helps adjust spanish text to line length adding hyphens.

    This is the main class of the task. It uses regular expressions
    and a set of simplified grammatical rules to split words.
    '''

    
    # Regular expressions for what is is considered a vowel and what
    # a consonant. It is not required that they are a single character.
    # Characters will be recognized as vowels before consonants when
    # there's ambiguity.
    vowel = r'(?:[aeiouáéíóúü]|y$)'
    consonant = r'(?:ch|ll|rr|[bcdfgjklmnñpqrstvwxyz])'
    
    # An attack group is a group of consonants that can start a syllable.
    # A coda group is a group of consonants that can end a syllable.
    attackGroup = r'(?:[pcbgf][rl]|[dt][r])|'# + consonant + r'h'
    codaGroup = r'(?:[bdmnlr]s|st])'
    # Excluded patterns
    excludeGroupCRE = re.compile(r'(?i)h')
    
    # Regular expression for finding a group of consonants between vowels.
    # This will serve to study if we can separate the word with an hyphen
    # here.
    splitPositions = re.compile(r'(?ri)((' + consonant + r')+)' + vowel)

    
    # Grammatical rules for splitting a group of consonants. They should
    # be considered in this order.
    rules = [
        re.compile(r'(?i)()' + consonant),
        re.compile(r'(?i)()' + attackGroup),
        re.compile(r'(?i)(' + consonant + r')' + consonant),
        re.compile(r'(?i)(' + consonant + r')' + attackGroup),
        re.compile(r'(?i)(' + codaGroup + r')' + consonant),
        re.compile(r'(?i)(' + codaGroup + r')' + attackGroup)
    ]    
    
    # Definition of what is a token (anything separated by spaces)
    # and a word (any string made of vowels and consonants)
    tokenCRE = re.compile(r'\S+')
    wordCRE = re.compile(r'(?ri)(?:' + consonant + r'|' + vowel + r')+')

    def __init__(self, lineLen):
        """Creates a SpanishFormatter with a specified line length.
        lineLen cannot be less than 10.
        """
        if lineLen < 10:
            raise ValueError('lineLen cannot be less than 10')
        self.len = lineLen
        self.currentSpace = lineLen
        self.beginningOfLine = True
    
    @classmethod
    def breakWord(cls, word, at):
        '''Returns the rightmost position not bigger than parameter
        at where an hyphen can be inserted. If there's not such a
        position, it returns 0.

        Example:
        The word alberto can be broken in 2 ways:
        al-berto
        alber-to
        breakWord('alberto', 5) would return 5
        breakWord('alberto', 4) would return 2
        breakWord('alberto', 1) would return 0
        '''
        for mat in cls.splitPositions.finditer(word):
            # Consonants at the beginning of the word
            # don't separate syllables (case mat.span()[0] == 0)
            if mat.span()[0] <= 0:
                continue
            if cls.excludeGroupCRE.fullmatch(mat[1]):
                continue

            # Default break position means couldn't apply rule
            breakPosition = -1
            for rule in cls.rules:
                applicable = rule.fullmatch(mat[1])
                if (applicable):
                    breakPosition = mat.span()[0]+len(applicable[1] or '')
                    break
            if breakPosition == -1:
                print(f'[{cls.__name__}] Cannot apply rule to group {mat[0]} in {word}', file=sys.stderr)
                # We could throw an exception here
                sys.exit(0)
            # You cannot leave a vowel alone at the end of a line
            # (case mat.span()[0] == 1)
            elif 0 < breakPosition <= at:
                return breakPosition
        return None

    @classmethod
    def breakToken(cls, token, at):
        '''Breaks a token -a sequence of non-space characters- in a pair of strings,
        where the first part hasn't got more characters than at and the split
        follows spanish rules.

        When no suitable break is available, the function returns None, token.

        For single words, use breakWord. breakToken is used for breaking apart
        words that may contain punctuation signs.
        '''
        for wordMatch in cls.wordCRE.finditer(token):
            division = cls.breakWord(wordMatch[0], at-wordMatch.span()[0])
            if division:
                breakAt = wordMatch.span()[0]+division
                return token[0:breakAt], token[breakAt:]
        return None, token


    def processLine(self, line, breakLine=True, file=sys.stdout):
        '''Processes a line of text, taking into account what is already written in
        the current line.

        The optinal parameter breakLine tells the class whether there should be a
        line break after this line or future lines should be processed as if they
        directly followed this line's last word.
        '''
        # Split at white space, process each word
        for token in self.tokenCRE.finditer(line):
            if self.currentSpace != self.len:
                # The token and a preceeding space may fit
                if len(token[0])+1 <= self.currentSpace:
                    print(' ', token[0], sep='', end='', file=file)
                    self.currentSpace-=len(token[0])+1
                # Or, we can insert a space, part of the token and a dash
                elif self.currentSpace > 2:
                    w1, w2 = self.breakToken(token[0], self.currentSpace-2)
                    if w1:
                        print(' ', w1, '-', sep='', file=file)
                    else:
                        print('', file=file)
                    print(w2, end='', file=file)
                    self.currentSpace = self.len-len(w2)
                # Or we should end this line and start another one
                else:
                    print('', file=file)
                    print(token[0], end='', file=file)
                    self.currentSpace = self.len-len(token[0])
                if self.currentSpace < 0:
                    print(f'[{self.__class__.__name__}] Exceptionally long word led to a bigger line.',
                        file=sys.stderr)
            else:
                # The first word goes without preceeding space
                print(token[0], end='', file=file)
                self.currentSpace -= len(token[0])
        
        if breakLine:
            print('', file=file)
            self.currentSpace = self.len




if __name__ == '__main__':
    # Testing of the module. Receives text file as an argument.
    name = sys.argv[1]

    # Files starting with the prefix 'words' will be treated as files
    # containing a single word in each line can be used to test the
    # function breakWord.
    # Files starting with the prefix 'text' will be treated as files
    # containing text that should be made to fit a line length. In that
    # case, the line length is specified as a second parameter.
    import os
    basename = os.path.basename(name)
    if basename.startswith('words'):
        file = open(name)
        txtForm = SpanishFormatter(10)
        for word in file:
            word = word[:-1]
            last = None
            print(word)
            for i in range(len(word)):
                at = txtForm.breakWord(word, i)
                if at != last:
                    last = at
                    print(word[0:at], '-', word[at:], sep='')
            print()
    elif basename.startswith('text'):
        file = open(name)
        lineLen = int(sys.argv[2])
        txtForm = SpanishFormatter(lineLen)
        for line in file:
            txtForm.processLine(line)




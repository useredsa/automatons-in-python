#!/usr/bin/python3
import regex as re
import sys

class TextFormatter(object):
    #TODO add description

    
    # Regular expressions for what is is considered a vowel and what
    # a consonant. It is not required that they are a single character.
    # Characters will be recognized as vowels before consonants when
    # there's ambiguity.
    vowel = r'(?:[aeiouáéíóú]|y$)'
    consonant = r'(?:ch|ll|rr|[bcdfghjklmnñpqrstvwxyz])'
    
    # An attack group is a group of consonants that can start a syllable.
    # A coda group is a group of consonants that can end a syllable.
    attackGroup = r'(?:[pcbgf](?:r|l)|(d|t)r)'
    codaGroup = r'(?:(?:b|d|m|n|l|r)s|st)'
    # We will be looking for attack groups starting from the end of a match.
    attackGroupCRE = re.compile(r'(?r)' + attackGroup)
    codaGroupCRE = re.compile(codaGroup)
    
    # Regular expression for finding a group of consonants between vowels.
    # This will serve to study if we can separate the word with an hyphen
    # here.
    splitPositions = re.compile(r'(?r)((' + consonant + r')+)' + vowel)

    
    # Grammatical rules for splitting a group of consonants. They should
    # be considered in this order.
    rules = [
        re.compile(r'()' + consonant),
        re.compile(r'()' + attackGroup),
        re.compile(r'(' + consonant + r')' + consonant),
        re.compile(r'(' + consonant + r')' + attackGroup),
        re.compile(r'(' + codaGroup + r')' + consonant),
        re.compile(r'(' + consonant + consonant + r')' + consonant + consonant)
    ]    
    
    # Definition of what is a token (anything separated by spaces)
    # and a word (any string made of vowels and consonants)
    tokenCRE = re.compile(r'\S+')
    wordCRE = re.compile(r'(?r)(?:' + consonant + r'|' + vowel + r')+')

    #TODO what is this?: pass
    def __init__(self, lineLen):
        """
        """
        self.len = lineLen
        self.currentSpace = lineLen
        self.beginningOfLine = True
    
    @classmethod
    def breakWord(cls, word, at):
        for mat in cls.splitPositions.finditer(word):
            # Consonants at the beginning of the word
            # don't separate syllables (case mat.span()[0] == 0)
            # You cannot leave a vowel alone at the end of a line
            # (case mat.span()[0] == 1)
            if mat.span()[0] <= 1:
                continue

            # Default break position means couldn't apply rule
            breakPosition = -1
            for rule in cls.rules:
                applicable = rule.fullmatch(mat[1])
                if (applicable):
                    breakPosition = mat.span()[0]+len(applicable[1])
                    break
            
            if breakPosition == -1:
                print(f'>> Cannot apply rule to group {mat[0]} in {word}', file=sys.stderr)
            elif breakPosition <= at:
                return breakPosition
        return 0

    @classmethod
    def breakToken(cls, token, at):
        for wordMatch in cls.wordCRE.finditer(token):
            division = cls.breakWord(wordMatch[0], at-wordMatch.span()[0])
            if division:
                breakAt = wordMatch.span()[0]+division
                return token[0:breakAt], token[breakAt:]
        return None, token

    def processToken(self, token):
        return 0

    def processLine(self, line, breakLine=True):
        # Split at white space, process each word
        for token in self.tokenCRE.finditer(line):
            if self.currentSpace != self.len:
                # The token and a preceeding space may fit
                if len(token[0])+1 <= self.currentSpace:
                    print(' ', token[0], sep='', end='')
                    self.currentSpace-=len(token[0])+1
                # Or, we can insert a space, part of the token and a dash
                elif self.currentSpace > 3:
                    w1, w2 = self.breakToken(token[0], self.currentSpace-2)
                    if w1:
                        print(' ', w1, '-', sep='')
                    else:
                        print()
                    print(w2, end='')
                    self.currentSpace = self.len-len(w2)
                else:
                    print()
                    print(token[0], end='')
                    self.currentSpace = self.len-len(token[0])
            # The first word goes without preceeding space
            else:
                print(token[0], end='')
                self.currentSpace -= len(token[0])
        
        if breakLine:
            print()
            self.currentSpace = self.len




#TODO comment main
if __name__ == '__main__':
    name = sys.argv[1]
    file = open(name)

    if name.startswith("words"):
        txtForm = TextFormatter(0)
        for word in file:
            word = word[:-1]
            last = 0
            print(word)
            for i in range(len(word)):
                at = txtForm.breakWord(word, i)
                if at != last:
                    last = at
                    print(word[0:at], '-', word[at:], sep='')
            print()
    elif name.startswith("text"):
        lineLen = int(input(), 10)
        txtForm = TextFormatter(lineLen)
        for line in file:
            txtForm.processLine(line)



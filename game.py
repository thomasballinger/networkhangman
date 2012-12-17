
ART = [
        """
     _____
     |   |
         |
         |
         |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
         |
         |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
     |   |
         |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
    /|   |
         |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
    /|\  |
         |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
    /|\  |
     |   |
         |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
    /|\  |
     |   |
    /    |
         |
   ______|____
""",
        """
     _____
     |   |
     O   |
    /|\  |
     |   |
    / \  |
         |
   ______|____
""",
]

class Hangman(object):

    def __init__(self):
        self.word = None
        self.guesses = 0
        self.misses = 0
        self.guessed = set()
        self.death_miss = 8

    def __str__(self):
        s = self.cur_art() + self.get_guessed_string()
        return s

    def display(self):
        s = ''
        if self.done():
            s += 'You win!'
        if self.misses >= self.death_miss:
            s += 'You lose!'
        s += str(self)
        return s

    def set_word(self, w):
        if self.word is None:
            self.word = w.lower()

    def guess(self, x):
        """Returns whether guess was a valid guess or not"""
        if self.word is None:
            return False
        if self.misses >= self.death_miss:
            return False
        x = x.lower()
        if x not in list('abcdefghijklmnopqrstuvwxyz'):
            return False
        if x in self.guessed:
            return False
        self.guessed.add(x)
        self.guesses += 1
        if x not in self.word:
            self.misses += 1
        return True

    def cur_art(self):
        return ART[self.misses]

    def get_guessed_string(self):
        if self.word:
            return " ".join(x if x in self.guessed else '_' for x in self.word)
        else:
            return 'No word yet'

    def done(self):
        return not any(x for x in self.word if x not in self.guessed)

if __name__ == '__main__':
    g = Hangman()
    g.set_word('snowy')
    while g.misses < g.death_miss:
        print g
        g.guess(raw_input('guess?'))
        if g.done():
            print 'you win!'
            break
    else:
        print 'you lose!'

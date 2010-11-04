
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import stdio
from twisted.protocols import basic
from itertools import count

import random

class Prompt(basic.LineReceiver):

    promptDeferred = None

    from os import linesep as delimiter

    def __call__(self, msg):
        return self.prompt(msg)

    def prompt(self, msg):
        assert self.promptDeferred is None
        self.display(msg+ '\n  ?  ')
        self.promptDeferred = defer.Deferred()
        return self.promptDeferred
    
    def display(self, msg):
        self.transport.write(msg )
    
    def lineReceived(self, line):
        # print "line received"
        if self.promptDeferred is None:
            return
        d, self.promptDeferred = self.promptDeferred, None
        d.callback(line)

class GuessGame(object):
    
    max_guesses = 3
    max_secret = 5
    _prompt = None

    def __init__(self, prompt):
        self.secret = random.randint(1, self.max_secret)
        self._prompt = prompt

        self.prompt = self._prompt.prompt
        self.display = self._prompt.display
        self.display(
            "Guess the secret number ! (max guesses: %s, max secret: %s)" 
            % ( self.max_guesses, self.max_secret))

    def check( self, guess ):
        
        if guess == self.secret:
            return ("won", '')

        if guess < 0 or  guess > self.max_secret:
            print "guess is %s, max_secret is %s" % (guess, self.max_secret)
            print "Is guess greater than max_secret? %s" % ( guess > self.max_secret )

            return ("miss",
                    'Remember, the number is between 0 and %s !' % self.max_secret)
                    
        else:
            status = "fail"
            reason = 'Too big' if guess > self.secret else 'Too small'

            if abs( guess - self.secret )==1:
                reason += ' Almost, though.'
        
            return (status, reason)
        
    def round(self, guess,count):
        status, reason = self.check(int(guess))
        
        if status == 'won':
            print "Good job, you guessed right in %s rounds" % str(count)
            reactor.stop()
        elif status == 'fail':
            if count >= self.max_guesses:
                print "Too many tries for this game, answer was %s" % self.secret
                reactor.stop()
            
        prompt(reason).addCallback(self.round, count+1)            


prompt = Prompt()
stdio.StandardIO(prompt)

# now through mails?, this means I have a client polling a mailbox (at
# some point I will have a server). Whenever a new mail arrive, 
# then I should make a file for the game and a file for each output.

# modify the imapclient to answer back when a matching email receives the message

# then maybe use different 

# think about involving superstar Fabrice

game = GuessGame(prompt)

game.display("\nChoosing random number between 1 and " 
      + str(game.max_secret) + ".\n...")

game.prompt("\nWhat do you think it is?\n").addCallback(game.round,1)


reactor.run()



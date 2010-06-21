#!/usr/bin/env python

# exercice 1
def reverses( l, r='' ):
    if len(l)==1:
        return l
    else:
        return l[-1] + reverses( l[:-1] )
# ''.join([c for c in reversed('coucou')])
    
def is_palindrome( word ):
    if word==reverses( word ):
        print "It is a palindrome"
        return True
    else:
        print "It is not a palindrome"
        return Flase

# exercice 2
def mystere( x, y ):
    if y==1:
        return x
    else:
        return x + mystere( x, y-1 )

is_mystere_multiplication=True

for x, y in (2, 3), (6, 7), (12, 34), (1000,1000):
    if x*y != mystere(x, y):
        is_mystere_multiplication=False
print "Is mystere the multiplication :", is_mystere_multiplication

def afficheChiffre(n):
    if n/10 == 0:
        return '/' + n
    else:
        return  afficheChiffre(n/10) + '/' + n % 10

# exercice 3
def add( x, y ):
    if x==1 and y==1:
        return 2
    elif x==1:
        return 1 + add( x, y-1 )
    else:
        return 1 + add( x-1, y )

def mult( n, m ):
    if m==1:
        return n
    else:
        return n + mult( n, m-1 )
        
    
# the boolean is_palindrome function is defined in exercice 1

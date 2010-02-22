#!/bin/env python
# -*- coding: utf-8 -*-

def myindex(t, reverse=False):

    ival = raw_input("Enter a value: ")

    if reverse:
        l = range( len(t)-1, 0, -1 )
    else:
        l = range( len(t) )

    for i in l:
        if int(ival) == t[i]:
            print( i+1 )
            return
    print('The value was not found')

def my_ord():

    val = raw_input("Enter a value (enter '$' when you're bored) : ")

    while val != '$':
        print ord(val)-ord('A')+1
        val = raw_input("Enter a value: ")
    
def upper():
    uppercase_distance = ord('A') - ord('a')

    t = ''
    for c in raw_input("Enter a string: "):
        if c==u'é' or c==u'è' or c==u'ê':
            print 'Mmmh weird'
            c =  'e'
        t += chr( ord(c) +  uppercase_distance )
    print t
                 
def frequence_relative():
    from collections import defaultdict

    d = defaultdict(int)
    for c in raw_input("Enter a string: "):
        d[c] += 1
    print d.items()

if __name__=="__main__":

    myindex([1,2,3,4,5,1,2,3,6,7,8,9])
    myindex([1,2,3,4,5,1,2,3,6,7,8,9], reverse=True)
    # Built in str.index()
    # print [1,2,3,4,5,1,2,3,6,7,8,9].index(2)
    # print [e for e in reversed([1,2,3,4,5,1,2,3,6,7,8,9])].index(2)
    my_ord()
    upper()   # does not work with 'coucoué' TODO
    frequence_relative()

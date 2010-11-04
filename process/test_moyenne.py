
from moyenne import moyenne

def positive():
    return moyenne(100)==50

def incorrect_test():
    return moyenne(100)==300

def zero():
    return moyenne(0)==0

def negative():
    return moyenne(-10)==-5

tests = "positive", "zero", "negative", "incorrect_test"

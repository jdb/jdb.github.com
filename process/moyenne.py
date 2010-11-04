

def moyenne(n):
    """Returns the mean of all numbers from 1 to n

    n is a positive integer, all hell breaks loose otherwise
    """
    k, s = 0, 0
    while k!=n+1:
        s+=k
        k+=1

    return s/n

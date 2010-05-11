
class counter(object):
    def __init__(start):
        self.count=start

    def __call__(jump=None):
        self.count = jump if jump else self.count+1


def counter(start=[0])
    start[0]+=1
    return start[0]


def counter(start=0):
    while 1:
        start+=1
        yield start


def counter(start=0):
    while 1:
        val = yield start+1
	start = val if val else start + 1

from twisted.internet.defer import Deferred

counter = [0]

def request():
    return Deferred()

def callback( counter ):
    for i in range(1000):
        counter[0]+=1

deferreds = [ request().addCallback(callback) for i in range(100) ] 

# There is a hundred concurrent actions pending, I can 
# execute the callback exactly whenever I want... 

# Now!

[ d.callback( counter ) for d in deferreds ]

print counter[0]

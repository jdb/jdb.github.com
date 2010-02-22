from bsddb import db

TS_SIZE=188
EXT3_PAGESIZE=4*1024

d = db.DB()
d.set_re_len(TS_SIZE)
d.set_pagesize(EXT3_PAGESIZE)
db.open('toto.db', None, DB_QUEUE, DB_CREATE|DB_THREAD)
db.append('tata')

from zope.interface import Interface, Attribute

class Icircularbuffer( Interface ):
    """Interface for the circular buffer"""

    source = Attribute("address and port of the live stream. ex: '224.0.0.1:1024'")
    length = Attribute("Maximum length of the circular buffer in minutes. ex: 120")
    size = Attribute("Maximum size on disk in GB. ex: 1")

    def play():
        """Plays the circular buffer. Starts a few seconds before live."""
        
    def pause():
        """Pause. When the current frame is about to be forgotten, then the stream is switched back to play"""

    def seek(date=None, offset=None):
        """Move the current position to the specified date. Date and offset are timestamps. The offset is used
        for relative seek"""

    def trickplay(scale):
        """Use this method to build the convenience functions fastforward, rewind, slow motion..."""


class circularbuffer:

    def __init__(self, source, duration_min=30, size_G=1 ):
        pass

    
    
    
# def_append
# _forget
# _init
# lire le paquet de telle date

# lecteur
# base qui s'initialise et qui offrent les methodes :

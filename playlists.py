#!/usr/bin/env python

from optparse import OptionParser

from os.path import isfile
from os import remove

from storm.locals import *
import sys

dbfile='playlists.db'
schemafile='playlists.sql'

def parse_args():
    """Available options"""
    usage = "Add playlist, remove playlist, play playlist, stop playlist"
    p = OptionParser( usage=usage )
    p.add_option('-a', '--add', help='label,ttlMode,StarWars,Dora,Spongebob')
    p.add_option('-r', '--remove', help='label')
    p.add_option('-p', '--play', help='label')
    p.add_option('-s', '--stop', help='label')
    return p.parse_args()

def initialise_database():

    if isfile(dbfile):
        store = Store( create_database('sqlite:%s' % dbfile) )
        return store
#    else
#         store = Store( create_database('sqlite:%s' % dbfile) )
#         store.execute( file(schemafile).read() )
#         store.commit()
#         return store



# class PlaylistStream(object):
#     __storm_table__ = 'PlaylistStreams'
#     id = Int(primary=True), 
#     id_playListInfo, currentPosition, currentContent = Int(), Int(), Int()

# class Playlist(object):
#     __storm_table__ = 'Playlists'
#     id = Int(primary=True)
#     label, maxEntries, ttlMode = RawStr(), Int(), RawStr()

#     def __init__(self, label, ttlMode='PERSISTENT', maxEntries=1000, ):

class ContentSegments(object):
    __storm_table__ = 'ContentSegments'
    name = RawStr(primary=True)
    startAt, stopAt = Int(), Int()

    def __init__(self, name, startAt, stopAt):
        

class Rights(object):
    __storm_table__ = 'Rights'
    contentSegments_name = RawStr()
    contentSegmentsName = Reference(contentSegments_name, ContentSegments.name)

    rewind, forward, seek, pause = RawStr(), RawStr(), RawStr(), RawStr()


if __name__ == '__main__':
    
    (o, args) = parse_args()
    db = initialise_database()

    if not db: sys.exit()

    if o.add:
        label, ttlMode = o.add.split(',')[:2] 
        contents = o.add.split(',')[2:] 
        db.add( ContentSegments() )


    elif o.play:
        playlist = db.find( Playlist, Playlist.label==o.remove).one()
        if playlist:
            db.add( PlaylistStream() )

    elif o.remove:
        db.remove( db.find( Playlist, Playlist.label==o.remove).one() )

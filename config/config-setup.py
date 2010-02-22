#!/bin/env python

# from ZODB.FileStorage import FileStorage
# from ZODB.DB import DB

import glob

# root = DB(FileStorage( 'Data.fs' )).open().root()

for i in glob.glob('interfaces/*.py'):
    __import__(i.replace('/','.').replace('.py',''))

print dir(interfaces)
    




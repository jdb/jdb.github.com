import pynotify
pynotify.init( "Some Application or Title" )

def  callback_function():
    print "Yooooooooooo"

n = pynotify.Notification("Title", "body\ntoto", "dialog-warning")
n.set_urgency(pynotify.URGENCY_NORMAL)
# n.set_timeout(pynotify.EXPIRES_NEVER)
# n.add_action("clicked","Button text", callback_function, None)
n.show()

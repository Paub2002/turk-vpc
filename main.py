import threading
import newUI
import server
import os
files = [
 'move_req.txt','move_res.txt',
 'hint_req.txt','hint_res.txt',
 'undo_req.txt','undo_res.txt',
]
dir = os.listdir()
for f in files: 
    if f in dir: os.remove(f) 

t1 = threading.Thread(target = newUI.run)
t2 = threading.Thread(target = server.runApp)
t1.start()
t2.start()
t1.join()
t2.join()
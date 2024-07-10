import threading
import UI
import server

from os import listdir, remove   #FS managment functions 

# List of filenames that are generated and deleted during execution and must be removed if left for some reason

files = [
 'move_req.txt','move_res.txt', # Move files
 'hint_req.txt','hint_res.txt', # Hint files
 'undo_req.txt','undo_res.txt', # Undo files
 'output.mp3'                   # Audio file 
]
# List of all directory content
dir = listdir()

#Check each file: 
for f in files: 
    if f in dir: remove(f)  #If exists remove it

#Initialize the thwo threads
t1 = threading.Thread(target = UI.run) # IA Main loop 
t2 = threading.Thread(target = server.runApp) # Server app 

#Start both threads
t1.start()
t2.start()

#End both threads
t1.join()
t2.join()
#!/usr/bin/env python2
import json
import os
import requests
from pandac.PandaModules import *

#due to packing and compiling,
#this module can only be accessed by devs,
#so its safe to debug here.

def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())

def openInjector():
    import Tkinter as tk
    from direct.stdpy import thread
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Toontown Journey Remote Debug Injector')
    root.resizable(False,False)
    global text
    frame = tk.Frame(root)
    text = tk.Text(frame,width=70,height=20)
    text.pack(side="left")
    tk.Button(root,text="Inject!",command=runInjectorCode).pack()
    scroll = tk.Scrollbar(frame)
    scroll.pack(fill="y",side="right")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame.pack(fill="y")

    thread.start_new_thread(root.mainloop,())

openInjector()

username = os.environ['ttiUsername']
password = os.environ['ttiPassword']
distribution = ConfigVariableString('distribution', 'dev').getValue()

accountServerEndpoint = ConfigVariableString(
    'account-server-endpoint',
    'https://toontownjourney.com/api/').getValue()
request = requests.post(
    accountServerEndpoint + 'login/',
    data={'n': username, 'p': password, 'dist': distribution})

try:
    response = json.loads(request.text)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if not response['success']:
        print response['reason']
    else:
        os.environ['TTI_PLAYCOOKIE'] = response['token']

        # Start the game:
        import toontown.toonbase.ClientStart

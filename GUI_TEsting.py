from Tkinter import *
import json
import urllib2



def login():

	userName = username.get()
	passwordIn = password.get()
	#url = "https://www.toontownunited.com/request.php?u=" + str(userName) + "&hash=" + str(passwordIn)
	url = "http://localhost/Non-Habbo/TTU/request.php?u=" + str(userName) + "&hash=" + str(passwordIn)
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)

	json_data = response.read().decode('utf-8')
	info = json.loads(json_data)

	print "Log: " + str(info)
	
	print "Log: JSON says hash is " + str(info['isCorrect'])
	if info['isCorrect'] == 1:
		print("Your password was correct")
	else:
		print("Incorrect password or username")


root = Tk()
username = StringVar()
password = StringVar()

root.title('Toontown United Launcher')

usernameEntry = Entry(root, textvariable=username).pack()
passEntry = Entry(root, textvariable=password, show="*").pack()

button = Button(root, text="Login!", command = login).pack()

root.mainloop()
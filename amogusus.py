import sys
sys.path.append('./Avoyd')
from setup import *
import tkinter as tk
import asyncio
#tk or tki...
tki = tk.Tk()
#tutorialllllllllll https://realpython.com/python-gui-tkinter/
tki.title("Avoyd!")
tki.geometry("350x350")
#random buffer button
button = tk.Button(
		text="A random buffer happens!",
		width=25,
		height=5,
		bg="blue",
		fg="yellow",
)
def eventHappen(bleh):
	randomBuffer()
button.bind("<ButtonRelease-1>", lambda event:eventHappen)
#manual buffer button
button2 = tk.Button(
		text="manual buffer!",
		width=25,
		height=5,
		bg="red",
		fg="green",
)
def eventHappen2(bleh):
	manualBuffer()
button2.bind("<ButtonRelease-1>", lambda event:eventHappen2)

#_____________________________________________________#
tester = False
name = False
askDriverName = tk.Entry(fg="yellow", bg="blue", width=25)
askDriverButton = tk.Button(
			text="enter",
			bg='grey',
			height=1,
		)
askDriverText = tk.Label(text = "Enter Virtual camera Driver Name")
def iWantToDie():
	button.pack()
	button2.pack()
	askDriverButton.pack_forget()
	askDriverName.pack_forget()
	askDriverText.pack_forget()
#askgin for virtual camera driver name
def thisSucks():
	if tester == False:
		askDriverName = tk.Entry(fg="yellow", bg="blue", width=25)
		#textbox
		#label/labels
		askDriverText = tk.Label(text = "Enter Virtual camera Driver Name")
		#"enter" button
		askDriverButton = tk.Button(
			text="enter",
			bg='grey',
			height=1,
		)
		def event(bleh):
			name = askDriverName.get()
			print(name)
			print("??????????????????????")
			iWantToDie()
		askDriverButton.bind("<ButtonRelease-1>", lambda event:event())

thisSucks()
  #________________________________________________#
  #GET THE NAME
# Set the position of button to coordinate (100, 20)
askDriverButton.place(x=150, y=170)
askDriverName.place(x=65, y=130)
askDriverText.pack()
tki.mainloop()

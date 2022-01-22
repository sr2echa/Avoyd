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
#_____________________________________________________#
tester = False
name = False
askDriverName = 'e'
askDriverButton = 'e'
askDriverText = 'e'
#askgin for virtual camera driver name
if not tester:
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
  def whatever():
    name = askDriverName.get()
    print(name)
  def event(bleh):
    whatever()
  askDriverButton.bind("<ButtonRelease-1>", event)

  #________________________________________________#
  #GET THE NAME
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
button.bind("<ButtonRelease-1>", eventHappen)
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
	#replace this with whatever YOU want!!!!!!!
button2.bind("<ButtonRelease-1>", eventHappen2)

# Set the position of button to coordinate (100, 20)
askDriverButton.pack()
askDriverButton.place(x=150, y=170)
askDriverName.place(x=65, y=130)
askDriverText.pack()
tki.mainloop()

import os
from turtle import color
import pyvirtualcam
import numpy as np
import cv2
import time
import random
import threading
from PIL import Image
from localStoragePy import localStoragePy
localStorage = localStoragePy('Avoyd')


import time
import sys
import trace
import threading

class KThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run     
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True





def setup():
    #default name of Virtual Camera
    global VCAM
    VCAM = input("Enter Virtual Camera Driver Name [Default(None) = 'Avoyd']: ")
    if VCAM == "":
        VCAM = "Avoyd"
    
    localStorage.setItem("VCAM",VCAM)

    with open("bat.bat","w") as f:
        f.write(f"""
@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
    regsvr32 "UnityCaptureFilter32bit.dll" "/i:UnityCaptureName={VCAM}"
    regsvr32 "UnityCaptureFilter64bit.dll" "/i:UnityCaptureName={VCAM}"
:--------------------------------------
""")

    os.system("bat.bat")
    os.remove('bat.bat')



#
#Virtual Camera 
#

def pixelate(img):
    # Resize smoothly down to 16x16 pixels
    imgSmall = img.resize((69,69),resample=Image.BILINEAR)
    # Scale back up using NEAREST to original size
    result = imgSmall.resize(img.size,Image.NEAREST)
    return result




#random buffer
def randombuffer():
    cap = cv2.VideoCapture(0)
    with pyvirtualcam.Camera(fps=20,width=1920, height=1080, device=str(localStorage.getItem("VCAM")), backend="unitycapture") as cam:
        #get the frame from built in camera and send it to the virtual camera using opencv
        frame=cap.read()[1]
        #frame=cam.get_frame()
        time.sleep(random.randint(1,20)/10)
        cam.send(np.array(pixelate(frame)))
        cam.sleep_until_next_frame()
'''
def manualbuffer():
    cap = cv2.VideoCapture(0)
    work = True
    with pyvirtualcam.Camera(fps=20,width=1920, height=1080, device=str(localStorage.getItem("VCAM")), backend="unitycapture") as cam:
        frame=cap.read()[1]
        if work==True:
            frame=cam.get_frame()
            cam.send(np.array(pixelate(frame)))
        cam.sleep_until_next_frame()
'''
def manualbuffer():
    cap = cv2.VideoCapture(0)
    work = True
    with pyvirtualcam.Camera(fps=20,width=1920, height=1080, device=str(localStorage.getItem("VCAM")), backend="unitycapture") as cam:
        frame=cap.read()[1]
        frame.save("frame.png")
        if work==True:
            #frame=cam.get_frame()
            cam.send(np.array(pixelate(frame)))
            cam.sleep_until_next_frame()
        else:
            while work==False:
                #frame=cam.get_frame()
                #cam.send frame.png from working directory
                f=open("frame.png","rb")
                cam.send(np.array(pixelate(f)))
                cam.sleep_until_next_frame()
        os.remove("frame.png")

def screencam():
    import pyautogui
    #from PIL import ImageGrab
    with pyvirtualcam.Camera(width=1920, height=1080, fps=60, backend="unitycapture") as cam:
        while True:
            #get the screenshot of the screen and send it to the virtual camera
            frame=pyautogui.screenshot()
            #frame = ImageGrab.grab()
            cam.send(np.array(frame))
            cam.sleep_until_next_frame()
            #print("Sending frame")

screencamcalc = 0

def modechk(mode):
    if mode == "1":
        print("MBC")
        manualbuffer_button()
    elif mode == "2":
        print("Auto Buffer")
        autobuffer_button()
    elif mode == "3":
        print("Screen Cam")
        screencam_button()



### Threadings ### 
def screencamchk():
    global screencamcalc
    if screencamcalc == 0:
        screencamcalc = 1
        button_4['text']='Stop'
        window.title("🟢 Avoyd - ScreenCam: ON")
        thread_screencam()
    else:
        screencamcalc = 0
        button_4['text']='Start'
        window.title("Avoyd - ScreenCam: OFF")
        kill_threads()
def thread_screencam():
    global screencamthread
    screencamthread=KThread(target=screencam)
    screencamthread.start()
def kill_threads():
    screencamthread.kill()
##################

##### Screencam Button #####
def screencam_button():
    ScreenCam_btn['image']=PhotoImage(
        file=relative_to_assets("SC_Active.png"))
    AutoBufferCam_btn['image']=PhotoImage(
        file=relative_to_assets("ABC_Deactive.png"))
    ManualBufferCam_btn['image']=PhotoImage(
        file=relative_to_assets("MBC_Deactive.png"))
    window.title("Avoyd - ScreenCam: OFF")
def autobuffer_button():
    img1=PhotoImage(
        file=relative_to_assets("SC_Deactive.png"))
    ScreenCam_btn['image']=img1

    img2=PhotoImage(
        file=relative_to_assets("ABC_Active.png"))
    AutoBufferCam_btn['image']=img2

    img3=PhotoImage(
        file=relative_to_assets("MBC_Deactive.png"))
    ManualBufferCam_btn['image']=img3

    window.title("Avoyd - AutoBuffer: OFF")
def manualbuffer_button():
    ScreenCam_btn['image']=None
    AutoBufferCam_btn['image']=None
    ManualBufferCam_btn['image']=None
    window.title("Avoyd - ManualBuffer: OFF")
    






#screencam()

def uninstall():
    with open("bat.bat","w") as f:
        f.write(r"""
@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
    regsvr32 /u "UnityCaptureFilter32bit.dll"
    regsvr32 /u "UnityCaptureFilter64bit.dll"
:--------------------------------------
""")
    os.startfile("bat.bat")
    os.remove('bat.bat')

    localStorage.removeItem("VCAM")
    localStorage.clear()



# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,LabelFrame


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("400x80")
window.configure(bg = "#000000")
window.title("Avoyd")


canvas = Canvas(
    window,
    bg = "#000000",
    height = 80,
    width = 400,
    bd = 0,
    highlightthickness = 0,
    relief = "flat"
)

canvas.place(x = 0, y = 0)
bg = PhotoImage(
    file=relative_to_assets("OptionMenu_Bg.png"))
OptionMenu_Bg = canvas.create_image(
    110.0,
    40.0,
    image=bg
)

border = LabelFrame(window, bd = 6, bg = "black")

button_image_1 = PhotoImage(
    file=relative_to_assets("MBC_Deactive.png"))
ManualBufferCam_btn = Button(
    border,
    image=button_image_1,
    highlightthickness=0,
    command=lambda: modechk("1"),
    relief="flat",
)
ManualBufferCam_btn.place(
    x=36.0,
    y=22.0,
    width=36.0,
    height=36.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("ABC_Deactive.png"))
AutoBufferCam_btn = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: modechk("2"),
    relief="flat"
)
AutoBufferCam_btn.place(
    x=91.0,
    y=22.0,
    width=36.0,
    height=36.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("SC_Deactive.png"))
ScreenCam_btn = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: screencam_button(),
    relief="flat"
)
ScreenCam_btn.place(
    x=146.0,
    y=22.0,
    width=36.0,
    height=36.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    273.0,
    40.0,
    image=image_image_2
)

#button_image_4 = PhotoImage(
    #file=relative_to_assets("button_4.png"))
button_4 = Button(
    text="Start",
    #colour="#ffffff",
    font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0",
    borderwidth=0,
    highlightthickness=0,
    command=lambda:screencamchk(),
    relief="flat"
    
)
button_4.place(
    x=219.0,
    y=22.0,
    width=110.0,
    height=36.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    364.0,
    40.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    364.0,
    40.0,
    image=image_image_4
)

button_image_5 = PhotoImage(
    file=relative_to_assets("Install_Button.png"))
Install_btn = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
Install_btn.place(
    x=348.0,
    y=24.0,
    width=32.0,
    height=32.0
)
window.resizable(False, False)

#if the window is closed, stop the threading
window.protocol("WM_DELETE_WINDOW",lambda: exit())
#stop a running thread


window.mainloop()

import os
import pyvirtualcam
import numpy as np
import cv2
import time
import random
from PIL import Image



def setup():
    #default name of Virtual Camera
    VCAM = input("Enter Virtual Camera Driver Name [Default(None) = 'Avoyd']: ")
    if VCAM == "":
        VCAM = "Avoyd"

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


cap = cv2.VideoCapture(0)

#random buffer
def randombuffer():
    with pyvirtualcam.Camera(fps=20,width=1920, height=1080,) as cam:
        #get the frame from built in camera and send it to the virtual camera using opencv
        frame=cap.read()[1]
        #frame=cam.get_frame()
        time.sleep(random.randint(1,20)/10)
        cam.send(np.array(pixelate(frame)))
        cam.sleep_until_next_frame()

def manualbuffer():
    work = True
    with pyvirtualcam.Camera(fps=20,width=1920, height=1080,) as cam:
        frame=cap.read()[1]
        if work==True:
            frame=cam.get_frame()
            cam.send(np.array(pixelate(frame)))
        cam.sleep_until_next_frame()


def screencam():
    import pyautogui
    #from PIL import ImageGrab
    with pyvirtualcam.Camera(width=1920, height=1080, fps=60) as cam:
        while True:
            #get the screenshot of the screen and send it to the virtual camera
            frame=pyautogui.screenshot()
            #frame = ImageGrab.grab()
            cam.send(np.array(frame))
            cam.sleep_until_next_frame()
            #print("Sending frame")

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


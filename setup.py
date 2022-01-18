import os

#default name of Virtual Camera
VCAM = input("Enter Virtual Camera Driver Name [Default(None) = 'Avoyd']: ")
if VCAM == "":
    VCAM = "Avoyd"


batchfile = f"""@echo off

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
"""

#execute cmds in cmd
os.system(eval(batchfile))


#
#Virtual Camera 
#

import pyvirtualcam
import numpy as np
import cv2
import time
import random
#import ffmpeg_streaming


cap = cv2.VideoCapture(0)

#random buffer
def randombuffer():
    with pyvirtualcam.Camera(fps=20, device=f'{VCAM}') as cam:
        #get the frame from built in camera and send it to the virtual camera using opencv
        frame=cap.read()[1]
        #frame=cam.get_frame()
        time.sleep(random.randint(1,20)/10)
        cam.send(frame)
        cam.sleep_until_next_frame()

def manualbuffer():
    work = True
    with pyvirtualcam.Camera(fps=20, device=f'{VCAM}') as cam:
        frame=cap.read()[1]
        if work==True:
            frame=cam.get_frame()
            cam.send(frame)
        cam.sleep_until_next_frame()

def screencam():
    #display the monitor screen on the virtual camera using ffmpeg
    with pyvirtualcam.Camera(fps=20, device=f'{VCAM}') as cam:
        #cam.send(ffmpeg_streaming.get_screen())
        cam.sleep_until_next_frame()

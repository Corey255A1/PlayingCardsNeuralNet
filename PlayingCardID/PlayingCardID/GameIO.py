from mss import mss
import pynput
import cv2
import numpy as np
from time import sleep
from queue import Queue
from threading import Thread

class GameIO:
    #Mouse and Keyboard Automation
    myMouse = pynput.mouse.Controller()
    myKeyboard = pynput.keyboard.Controller()
    keylistener = None
    sct = mss()
    monitor = 0
    startX = 0
    endX = 0
    startY = 0
    endY = 0
    keyPressQueue = Queue()
    keyPressThreadRunning = False
    keyPressThread = None
    KeyCallback = {}

    def AddKeyPressCallback(self, key, func):
        key = "\'"+key+"\'"
        if(key not in self.KeyCallback):
            self.KeyCallback[key] = []
        self.KeyCallback[key].append(func)

    def __onKeyDown(self, key):
        print('{0}'.format(key))

    def __onKeyUp(self,key):
        k = '{0}'.format(key)
        print("Up" + k)
        if(k in self.KeyCallback):
            for func in self.KeyCallback[k]:
                func()

    def BeginKeyListner(self):
        keylistener = pynput.keyboard.Listener(on_press=self.__onKeyDown, on_release=self.__onKeyUp)
        keylistener.start()
    
    def GrabScreen(self):
        return np.array(self.sct.grab(self.sct.monitors[self.monitor]))

    def GrabRegion(self,startx=None, endx=None, starty=None, endy=None):
        if startx is None: startx = self.startX
        if starty is None: starty = self.startY
        if endx is None: endx = self.endX
        if endy is None: endy = self.endY
        return self.GrabScreen()[starty:endy,startx:endx]

    def DefineScreenRegion(self, monitor):
        self.monitor = monitor
        (x,y,w,h) = cv2.selectROI("grabber",self.GrabScreen())
        cv2.destroyWindow("grabber")
        if(x==0 and y==0 and w==0 and h==0):
            return False
        self.startX = int(x)
        self.endX = int(x)+int(w)
        self.startY = int(y)
        self.endY = int(y)+int(h)
        return True

    #MOUSE
    def MouseMove(self,x,y,screenRegionOffset=False,absolute=False):
        if screenRegion:
            x=x+self.startX
            y=y+self.startY

        if absolute:
            pos = self.myMouse.position
            self.myMouse.move(x-pos[0],y-pos[1])
        else:
            self.myMouse.move(x,y)

    def MouseClick(self):
        self.myMouse.click()

    def MousePress(self):
        self.myMouse.press()

    def MouseRelease(self):
        self.myMouse.release()

    #KEYBOARD
    def SendAsyncKey(self, key, delay):
        self.keyPressQueue.put((key,delay))

    def SendKey(self, key, delay):
        self.myKeyboard.press(key)
        sleep(delay)
        self.myKeyboard.release(key)

    def PressKey(self, key):
        self.myKeyboard.press(key)

    def ReleaseKey(self,key):
        self.myKeyboard.release(key)

    def StartAsyncKeyThread(self):
        self.keyPressThread = Thread(target=self.__keyPressThread)
        self.keyPressThread.daemon = True
        self.keyPressThreadRunning = True
        self.keyPressThread.start()

    def StopAsyncKeyThread(self):
        self.keyPressThreadRunning = False
        self.keyPressThread.join()
        self.keyPressThread = None

    def __keyPressThread(self):
        while self.keyPressThreadRunning:
            q = self.keyPressQueue.get()
            self.myKeyboard.press(q[0])
            sleep(q[1])
            self.myKeyboard.release(q[0])


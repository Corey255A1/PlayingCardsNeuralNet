import pandas as pd
import numpy as np
#load our saved model
from keras.models import load_model
from keras.datasets import mnist
import os
import cv2


#Find the Max and Second Max valu in an array
def getMaxIndex(lbls):
    indx = 0
    maxindx = 0
    secmaxindx = 0
    max = 0
    secmax = 0

    for l in lbls[0]:
        if l > max:
            secmax=max
            secmaxindx=maxindx
            max=l
            maxindx=indx
        elif l > secmax:
            secmax=l
            secmaxindx=indx        
        indx+=1
    return (maxindx,secmaxindx)


#Playing Card Images
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
H_WIDTH = int(IMAGE_WIDTH/2)
H_HEIGHT = int(IMAGE_HEIGHT/2)


FRAME_GRAB_W = 350 
FRAME_GRAB_H = 400
FH_WIDTH = int(FRAME_GRAB_W/2)
FH_HEIGHT = int(FRAME_GRAB_H/2)

IMAGE_CHANNELS = 1

NUMBER_OF_CLASSES=52


#Load the Model
model = load_model('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\PlayingCardID\\PlayingCardID\\model-018.h5')
trainraw = pd.read_csv('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\Cards.txt')

filenames = trainraw['FILENAME'].values
ids = trainraw['ID'].values

# Capture from first Camera Source
cap = cv2.VideoCapture(0)




while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    cH = int(height/2)
    cW = int(width/2)
    modImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crop the Image
    frontFrame = modImg[cH-FH_HEIGHT:cH+FH_HEIGHT,cW-FH_WIDTH:cW+FH_WIDTH]
    frontFrame = cv2.resize(frontFrame,(IMAGE_WIDTH,IMAGE_HEIGHT))
    # Get Weights of Classes
    lbl = model.predict(np.reshape(frontFrame,(1,IMAGE_WIDTH,IMAGE_HEIGHT,IMAGE_CHANNELS)),batch_size=1)

    cardnames = trainraw['CARD'].values
    (max,secmac) = getMaxIndex(lbl)


    cv2.rectangle(frame,(cW-FH_WIDTH,cH-FH_HEIGHT),(cW+FH_WIDTH,cH+FH_HEIGHT),(255,0,0))
    cv2.putText(frame,cardnames[max],(0,height-10),cv2.FONT_HERSHEY_PLAIN,8,(0,255,0))
    cv2.imshow('img',frame)
    
    # Adjust WaitKey Time if Frames are Freezing
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
import pandas as pd
import numpy as np
#load our saved model
from keras.models import load_model
#from keras.datasets import cifar100
#from keras.datasets import cifar10
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
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
IMAGE_CHANNELS = 1

#NUMBER_OF_CLASSES=52
NUMBER_OF_CLASSES=2

#GET Canned IMAGE
img = cv2.imread('D:\\Documents\\ImageProjects\\Queen.jpg',cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(IMAGE_WIDTH,IMAGE_HEIGHT))


cv2.imshow("Image to Predict",img)
cv2.waitKey()

#Load the Model
model = load_model('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\PlayingCardID\\PlayingCardID\\EvenBetterModel.h5')

# Get Weights of Classes
lbl = model.predict(np.reshape(img,(1,IMAGE_WIDTH,IMAGE_HEIGHT,IMAGE_CHANNELS)),batch_size=1)

#Find the Max Value for a class
Percentages = []

for l in lbl[0]:
    print(l)

trainraw = pd.read_csv('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\Cards.txt')

filenames = trainraw['FILENAME'].values
ids = trainraw['ID'].values

cardnames = trainraw['CARD'].values
(max,secmac) = getMaxIndex(lbl)
print(str(max)+ " " + str(lbl[0][max]) + " " + cardnames[max])

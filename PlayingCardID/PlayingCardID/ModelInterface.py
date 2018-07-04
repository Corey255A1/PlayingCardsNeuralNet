import pandas as pd
import numpy as np
#load our saved model
from keras.models import load_model
from keras.datasets import mnist
import os
import cv2


class ModelIF:
    #Playing Card Images
    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128
    H_WIDTH = int(IMAGE_WIDTH/2)
    H_HEIGHT = int(IMAGE_HEIGHT/2)
    IMAGE_CHANNELS = 1
    NUMBER_OF_CLASSES=52
    
    def __init__(self, model, **kwargs):
        #model = load_model('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\PlayingCardID\\PlayingCardID\\model-018.h5')
        self.MyModel = load_model(model)
        self.TrainingLabels = pd.read_csv('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\Cards.txt')
        #self.CardFileNames = trainraw['FILENAME'].values
        #self.CardIDs = trainraw['ID'].values
        self.CardNames = self.TrainingLabels['CARD'].values
        return super().__init__(**kwargs)

    #Find the Max and Second Max valu in an array
    def __getMaxIndex(self,lbls):
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

    def GetCardIndex(self,img):
        rimg = cv2.resize(img,(self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        #rimg=cv2.GaussianBlur(rimg,(3,3),0.8)
        #cv2.imshow("sized",rimg)
        #cv2.waitKey()
        # Get Weights of Classes
        lbl = self.MyModel.predict(np.reshape(rimg,(1,self.IMAGE_WIDTH,self.IMAGE_HEIGHT,self.IMAGE_CHANNELS)),batch_size=1)
        (max,secmac) = self.__getMaxIndex(lbl)
        return int(max)

    def GetCardName(self,index):
        return self.CardNames[index]
    

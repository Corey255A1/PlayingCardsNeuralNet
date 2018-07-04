import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.optimizers import Adam, SGD
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten, BatchNormalization

from keras.utils import to_categorical
import os
import cv2
from random import *


#LEARNING_RATE=1.0e-4
LEARNING_RATE=1.0e-4
SAMPLES_PER_EPOCH=3000
NUMBER_OF_EPOCHS=20
BATCH_SIZE=64
SAVE_BEST_ONLY='true'
KEEP_PROBABILITY=0.65

#Playing Card Images
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
HIMG_H = int(IMAGE_HEIGHT/2)
HIMG_W = int(IMAGE_WIDTH/2)
#IMAGE_CHANNELS = 3
IMAGE_CHANNELS = 1

NUMBER_OF_CLASSES=52
#NUMBER_OF_CLASSES=2


def build_model():
    model = Sequential()

    model.add(Conv2D(32, 5,5, activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)))
    model.add(BatchNormalization())

    model.add(Conv2D(32, 3,3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(KEEP_PROBABILITY))

    model.add(Conv2D(16, 3,3, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(KEEP_PROBABILITY))

    model.add(Conv2D(16, 1,1, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(KEEP_PROBABILITY))

    model.add(Flatten())
    model.add(Dense(128,activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(KEEP_PROBABILITY))

    model.add(Dense(64,activation='relu'))
    model.add(Dense(NUMBER_OF_CLASSES,activation='softmax'))
    model.summary()

    return model

def train_model(model, X_train, X_valid, Y_train, Y_valid): 
    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                monitor='val_loss', 
                                verbose=0, 
                                save_best_only=SAVE_BEST_ONLY,
                                mode='auto')

    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=LEARNING_RATE), metrics=['accuracy'])
    #model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=LEARNING_RATE), metrics=['accuracy'])
    model.fit_generator(Yielder(X_train,Y_train,True), 
                        SAMPLES_PER_EPOCH, 
                        NUMBER_OF_EPOCHS, 
                        max_q_size=1, 
                        validation_data=Yielder(X_valid,Y_valid,False), 
                        nb_val_samples=len(X_valid),
                        callbacks=[checkpoint],
                        verbose=1)




BASE = np.float32([[0,0],[0,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,0]])
SIZE = np.float32([[10,10],[10,IMAGE_HEIGHT-11],[IMAGE_WIDTH-11,IMAGE_HEIGHT-11],[IMAGE_WIDTH-11,10]])
SIZE2 = np.float32([[15,15],[15,IMAGE_HEIGHT-16],[IMAGE_WIDTH-16,IMAGE_HEIGHT-16],[IMAGE_WIDTH-16,15]])
SIZE3 = np.float32([[20,20],[20,IMAGE_HEIGHT-21],[IMAGE_WIDTH-21,IMAGE_HEIGHT-21],[IMAGE_WIDTH-21,20]])

LEFT_SQUISH = np.float32([[0,10],[0,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,0]])
RIGHT_SQUISH = np.float32([[0,0],[0,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,IMAGE_HEIGHT-11],[IMAGE_WIDTH-1,10]])
TOP_SQUISH = np.float32([[10,0],[0,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,IMAGE_HEIGHT-1],[IMAGE_WIDTH-11,0]])
BOTTOM_SQUISH = np.float32([[0,0],[10,IMAGE_HEIGHT-1],[IMAGE_WIDTH-11,IMAGE_HEIGHT-1],[IMAGE_WIDTH-1,0]])


LEFT_SQUISH_TRANS = cv2.getPerspectiveTransform(BASE,LEFT_SQUISH)
RIGHT_SQUISH_TRANS = cv2.getPerspectiveTransform(BASE,RIGHT_SQUISH)
TOP_SQUISH_TRANS = cv2.getPerspectiveTransform(BASE,TOP_SQUISH)
BOTTOM_SQUISH_TRANS = cv2.getPerspectiveTransform(BASE,BOTTOM_SQUISH)

ZOOM_IN = cv2.getPerspectiveTransform(SIZE,BASE)
ZOOM_IN2 = cv2.getPerspectiveTransform(SIZE2,BASE)
ZOOM_IN3 = cv2.getPerspectiveTransform(SIZE3,BASE)
ZOOM_OUT  = cv2.getPerspectiveTransform(BASE,SIZE)

def augment(img):
    nimg = img

    #30% of the time, no augmentation
    if np.random.rand() >= 0.7:
        return nimg

    #ROTATE 180
    if np.random.rand() < 0.5:
        nimg = cv2.flip(nimg,-1) #0 Around X, 1 around Y, -1 around both (180 rotation)

    #SLIGHT ROTATION
    rot = np.random.rand()*4.0
    if np.random.rand() < 0.5:
        rot = -rot

    center = tuple(np.array(nimg.shape[1::-1])/2)
    m = cv2.getRotationMatrix2D(center,rot,1.0)
    nimg = cv2.warpAffine(nimg,m,img.shape[1::-1])

    #DARKNESS OR LIGHTNESS
    dob = np.random.rand()
    if(dob < 0.33):
        nimg = cv2.subtract(nimg,np.array([np.random.rand()*90.0]))
    elif(dob > 0.66):
        nimg = cv2.add(nimg,np.array([np.random.rand()*90.0]))
    elif(dob > 0.4):
        _, nimg = cv2.threshold(nimg,128,255,cv2.THRESH_BINARY)
    

    #PERSPECTIVE
    persp = np.random.rand()
    if(persp > 0.9):
        nimg = cv2.warpPerspective(nimg,TOP_SQUISH_TRANS,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(persp > 0.8):
        nimg = cv2.warpPerspective(nimg,BOTTOM_SQUISH_TRANS,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(persp > 0.7):
        nimg = cv2.warpPerspective(nimg,LEFT_SQUISH_TRANS,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(persp > 0.6):
        nimg = cv2.warpPerspective(nimg,RIGHT_SQUISH_TRANS,(IMAGE_WIDTH,IMAGE_HEIGHT))

    #SCALE
    scaler = np.random.rand()
    if(scaler>0.9):
        nimg = cv2.warpPerspective(nimg,ZOOM_IN3,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(scaler>0.8):
        nimg = cv2.warpPerspective(nimg,ZOOM_IN2,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(scaler>0.6):
        nimg = cv2.warpPerspective(nimg,ZOOM_IN,(IMAGE_WIDTH,IMAGE_HEIGHT))
    elif(scaler<0.2): 
        nimg = cv2.warpPerspective(nimg,ZOOM_OUT,(IMAGE_WIDTH,IMAGE_HEIGHT))


    #OBSTRUCTION
    #obst = np.random.rand()
    #if(obst>0.95):
    #    rx = int(IMAGE_WIDTH*np.random.rand())
    #    ry = int(IMAGE_HEIGHT*np.random.rand())
    #    rw = int(5*np.random.rand()+5)
    #    rh = int(5*np.random.rand()+5)
    #    rc = int(255*np.random.rand())
    #    points = np.array([[rx,ry],[rx+rw,ry],[rx+rw,ry+rh],[rx,ry+rh]])
    #    img = cv2.fillPoly(img,[points],(rc,rc,rc))


    #BLUR
    blurry = np.random.rand()
    if(blurry > 0.9):
        nimg = cv2.GaussianBlur(nimg,(5,5),blurry)
    elif(blurry > 0.7):
        nimg = cv2.GaussianBlur(nimg,(3,3),blurry)


    #cv2.imshow('card2',np.array(nimg,dtype='uint8'))
    #cv2.waitKey(200)
    return nimg

def Yielder(x,y,aug):
    xBatch = np.empty([BATCH_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    yBatch = np.empty([BATCH_SIZE, NUMBER_OF_CLASSES])
    while True:
        i = 0
        # Shuffle up the data sets to get good mixes when training
        for index in np.random.permutation(len(x)):
            if aug:
                xBatch[i] = np.reshape(augment(x[index]),(IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS))
            else:
                xBatch[i] = np.reshape(x[index],(IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS))

            yBatch[i] = y[index]
            #cv2.imshow('card2',np.array(xBatch[i],dtype='uint8'))
            #cv2.waitKey(200)
            i+=1
            if i == BATCH_SIZE:
                break
        cv2.destroyWindow('card2')
        # Every loop of this While, yields a new batch to the fit function
        yield xBatch, yBatch

#(X_train, Y_train), (X_valid, Y_valid) = mnist.load_data()

cardPaths = []
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards1")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards2")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards3")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards4")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards5")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards6")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards7")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards8")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards9")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards10")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards11")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards12")
cardPaths.append("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards13")
CardImages = []
CardIDs = []


trainraw = pd.read_csv('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\Cards.txt')

filenames = trainraw['FILENAME'].values
ids = trainraw['ID'].values
cardnames = trainraw['CARD'].values

for cardpath in cardPaths:
    currCard = 0
    fnames = os.listdir(cardpath)
    imgs = []
    for imgName in filenames:
        p = cardpath+"\\"+imgName
        img = cv2.imread(p,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(IMAGE_WIDTH,IMAGE_HEIGHT))
        cv2.imshow('card',img)
        cv2.waitKey(30)
        #reshape because that is what the neuralnet wants
        #add to the X set
        #shaped = np.reshape(img,(IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS))
        #cv2.imshow('card',img)
        #cv2.waitKey()
        CardImages.append(img)
        #specify what letter this character is in the Y set
        cats = [0]*NUMBER_OF_CLASSES
        cats[currCard] = 1
        currCard = currCard + 1
        CardIDs.append(cats)

cv2.destroyWindow('card')
#Categories are in the form of [1,0,0....0,0] meaning A
#cv2.imshow('randomsample',CardImages[299])
#cv2.waitKey()
#for i in range(0,NUMBER_OF_CLASSES):
#    if(CardIDs[299][i] == 1):
#        print("THIS IS THE VALUE:" + str(i)+ " " + cardnames[i])



#split images into training and validation sets
X_train, X_valid, Y_train, Y_valid = train_test_split(CardImages,CardIDs)

the_model = build_model()
train_model(the_model,X_train,X_valid,Y_train,Y_valid)


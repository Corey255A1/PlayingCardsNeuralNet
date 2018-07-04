import pandas as pd
import numpy as np
import os
import cv2
import GameIO
from CardExtraction import SolitaireCardExtractor
import ModelInterface


HomeBase = {"spades":0,
            "diamonds":0,
            "clubs":0,
            "hearts":0}
DrawPile = []
Spread = []

modelIF = ModelInterface.ModelIF('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\PlayingCardID\\PlayingCardID\\ProbablyBest.h5')
gameIO = GameIO.GameIO()

cardExt = SolitaireCardExtractor()
gameIO.DefineScreenRegion(1)

while True:
    playingfield = gameIO.GrabRegion()

    #Returns a dictionary of card types and (theImage,(centerX,centerY))
    cards = cardExt.GetCurrentCards(playingfield)

    for c in cards:    
        card = cards[c]
        #(theImage,(centerX,centerY))
        cv2.GaussianBlur(card[0],(3,3),0.3)
        idx = modelIF.GetCardIndex(card[0])
        cv2.putText(playingfield, modelIF.GetCardName(idx), card[1], cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        cv2.putText(playingfield, modelIF.GetCardName(idx), card[1], cv2.FONT_HERSHEY_PLAIN,2.3,(255,0,0),2)
        #cv2.imwrite('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\cards12\\'+modelIF.GetCardName(idx)+'.jpg',card[0])

    cv2.imshow("Labeled",playingfield)
    #cv2.imshow("card",cards[SolitaireCardExtractor.DRAWPILE][0])
    # Adjust WaitKey Time if Frames are Freezing
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break


import cv2
import numpy as np

class ThreshVal:
    __upper = 0
    __lower = 0
    def __init__(self, val, thresh):
       self.__upper = val + thresh
       self.__lower = val - thresh

    def inRange(self,val):
        return (val>self.__lower and val<self.__upper)

class SolitaireCardExtractor:
    __HueThreshL = 0
    __SaturationThreshL = 0
    __LuminanceThreshL = 190
    __HueThreshH = 190
    __SaturationThreshH = 122
    __LuminanceThreshH = 255
    __lower_thresh = np.array([__HueThreshL,__SaturationThreshL,__LuminanceThreshL])
    __upper_thresh = np.array([__HueThreshH,__SaturationThreshH,__LuminanceThreshH])
    __cardWidth = 120
    __cardHeight = 160
    TOP_ROW_Y = 200
    DRAWPILE_X = ThreshVal(343,100)
    H1_X = ThreshVal(597,50)
    H2_X = ThreshVal(747,50)
    H3_X = ThreshVal(898,50)
    H4_X = ThreshVal(1048,50)

    C1_X = ThreshVal(147,50)
    C2_X = ThreshVal(296,50)
    C3_X = ThreshVal(447,50)
    C4_X = ThreshVal(597,50)
    C5_X = ThreshVal(747,50)
    C6_X = ThreshVal(898,50)
    C7_X = ThreshVal(1048,50)

    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    DRAWPILE = "d"
    C1 = "c1"
    C2 = "c2"
    C3 = "c3"
    C4 = "c4"
    C5 = "c5"
    C6 = "c6"
    C7 = "c7"

    def __getImageMask(self,img):
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv,(15,15),0)
        mask = cv2.inRange(hsv, self.__lower_thresh, self.__upper_thresh)
        mask = cv2.erode(mask,(5,5),iterations=4)
        #cv2.imshow("mask",mask)
        #cv2.waitKey()
        return mask

    def __getBoundingRects(self,mask):
        (im2, conts, ret) = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in conts:
            p = cv2.arcLength(c,True)
            if p > 500:
                a = cv2.approxPolyDP(c,0.03*p,True)
                if len(a) >= 4: #Four Points
                    (x,y,w,h) = cv2.boundingRect(a)
                    #Account for vertical card stack
                    if h>self.__cardHeight:
                        y=(y+h)-self.__cardHeight
                        h=self.__cardHeight
                    #Account for horizontal card stack
                    if w>self.__cardWidth:
                        x=(x+w)-self.__cardWidth
                        w=self.__cardWidth
                    yield (x,y,w,h)        


    def GetCurrentCards(self,img):
        mask = self.__getImageMask(img)
        cardmap = {}
        for (x,y,w,h) in self.__getBoundingRects(mask):
            extract = img[y:y+h,x:x+w]
            #cv2.imshow("extract",extract)
            #cv2.waitKey()
            cX = x+(w/2)
            cY = y+(h/2)
            mapval = ""
            if cY<self.TOP_ROW_Y:
                if self.DRAWPILE_X.inRange(cX): mapval = self.DRAWPILE
                elif self.H1_X.inRange(cX):mapval = self.H1
                elif self.H2_X.inRange(cX):mapval = self.H2
                elif self.H3_X.inRange(cX):mapval = self.H3
                elif self.H4_X.inRange(cX):mapval = self.H4
            else:
                if self.C1_X.inRange(cX): mapval = self.C1
                elif self.C2_X.inRange(cX):mapval = self.C2
                elif self.C3_X.inRange(cX):mapval = self.C3
                elif self.C4_X.inRange(cX):mapval = self.C4
                elif self.C5_X.inRange(cX):mapval = self.C5
                elif self.C6_X.inRange(cX):mapval = self.C6
                elif self.C7_X.inRange(cX):mapval = self.C7

            gray = cv2.cvtColor(extract,cv2.COLOR_BGR2GRAY)
            #_, gray = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
            cardmap[mapval] = (gray,(int(cX),int(cY)))
        return cardmap
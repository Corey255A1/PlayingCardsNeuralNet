import cv2
import numpy as np

class Basket:
    def __init__(self,lower,upper):
        self.LowerThresh = lower
        self.UpperThresh = upper
        self.Values = []
    def CheckRange(self,val):
        return (val>self.LowerThresh and val<self.UpperThresh)
    
    def AddValue(self,val):
        self.Values.append(val)

    def GetAverage(self):
        return int(sum(self.Values)/len(self.Values))


cardName = "cards8"
img = cv2.imread("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\"+cardName+".jpg")
gimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gimg = cv2.GaussianBlur(gimg,(3,3),0)
ret, thresh = cv2.threshold(gimg, 160, 255, cv2.THRESH_BINARY_INV)

thresh = cv2.dilate(thresh,(3,3),iterations=1)
#lines = cv2.HoughLinesP(thresh,1,np.pi/180,200,minLineLength=200,maxLineGap=10)
linesH = cv2.HoughLinesP(thresh,1,np.pi/2,900,minLineLength=1800,maxLineGap=20)
linesV = cv2.HoughLinesP(thresh,1,np.pi,100,minLineLength=800,maxLineGap=10)
alllines = [linesH,linesV]

cv2.imshow("cards",thresh)
cv2.waitKey()

YBasket = []
XBasket = []

lineWidth = 90

for lines in alllines:
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            foundY = False
            for yb in YBasket:
                if(yb.CheckRange(y1)):
                    yb.AddValue(y1)
                    foundY = True
                    break
            if(not foundY):
                yb = Basket(y1-lineWidth,y1+lineWidth)
                yb.AddValue(y1)
                YBasket.append(yb)

            foundX = False
            for xb in XBasket:
                if(xb.CheckRange(x1)):
                    xb.AddValue(x1)
                    foundX = True
                    break
            if(not foundX):
                xb = Basket(x1-lineWidth,x1+lineWidth)
                xb.AddValue(x1)
                XBasket.append(xb)

            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

YBasket.sort(key=lambda x: x.GetAverage())
XBasket.sort(key=lambda x: x.GetAverage())

slice = 0
#for y in range(0,len(YBasket)-1):
#    for x in range(0,len(XBasket)-1):
#        cv2.imwrite("D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\"+cardName+"\\"+str(slice)+".jpg",img[YBasket[y].GetAverage():YBasket[y+1].GetAverage(),XBasket[x].GetAverage():XBasket[x+1].GetAverage()])
#        slice = slice + 1

cv2.imshow("cards",img)
cv2.waitKey()

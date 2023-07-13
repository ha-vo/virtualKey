import cv2
import numpy as np

from HandTracking import handDetector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

handDetector = handDetector()

listCharacter = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G',
                 'H','J','K','L',';','Z','X','C','V','B','N','M',',','.','/']

x, y = 100, 100
class Button:
    def __init__(self, pos, chrt, size = [85, 85] ):
        self.pos = pos
        self.chrt = chrt
        self.size = size

listButton = []
i = 0

while i < len(listCharacter):
    btn = Button([x,y],listCharacter[i])
    listButton.append(btn)
    x += 100
    if x >= 1100:
        x = 100
        y += 100
    i += 1

def drawKeyBoard(img, listButton):
    for btn in listButton:
        x1, y1 = btn.pos
        x2 = btn.pos[0] + btn.size[0]
        y2 = btn.pos[1] + btn.size[1]
        cv2.rectangle(img,[x1,y1] ,[x2,y2],(0,0,0), cv2.FILLED)
        cv2.putText(img, btn.chrt, (x1+20, y1+60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img

textOuput = ''
while True:
    _, img = cap.read()
    img = handDetector.findHands(img)
    positions = handDetector.findPosition(img)
    img = drawKeyBoard(img,listButton)
    cv2.rectangle(img, [320, 450], [960, 550], (0, 0, 0), cv2.FILLED)
    cv2.putText(img, textOuput, (320 + 50, 450 + 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    if positions:
        for btn in listButton:
            x, y = btn.pos
            print(x, y, positions[8])
            if x < positions[8][1] < x + 85 and y < positions[8][2] < y + 85:
                cv2.rectangle(img, [x, y], [x + 85, y + 85], (255, 0, 0), cv2.FILLED)
                cv2.putText(img, btn.chrt, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                distance = np.hypot(positions[12][1]- positions[8][1], positions[12][2] - positions[8][2])

                if distance < 50:
                    cv2.rectangle(img, [x, y], [x + 85, y + 85], (255, 255, 0), cv2.FILLED)
                    textOuput += btn.chrt




    cv2.imshow("img", img)
    if cv2.waitKey(1) and 0xff == 'q':
        break


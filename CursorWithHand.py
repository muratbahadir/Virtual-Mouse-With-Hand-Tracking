import cv2
import HandDetectionModule as hs
import time
import autopy
import numpy as np
import math as m

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0



def MouseControl(lmList, bbox, img):
    h, w, c = img.shape
    wScr, hScr = autopy.screen.size()
    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    print(area)
    cv2.circle(img, (lmList[8][1], lmList[8][2]), 15, (255, 0, 255), cv2.FILLED)
    cv2.circle(img, (lmList[8][1], lmList[8][2]), 15, (255, 0, 255), cv2.FILLED)
    try:
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]
        sonuc = m.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
        if area > 20000:
            x = np.interp(lmList[8][1], (0, w), (0, wScr))
            y = np.interp(lmList[8][2], (0, h), (0, hScr))

        else:
            x = np.interp(lmList[8][1], (w / 4, 3 * w / 4), (0, wScr))
            y = np.interp(lmList[8][2], (h / 4, 3 * h / 4), (0, hScr))

        autopy.mouse.move(x, y)
        if sonuc / area < 0.001:
            print("Tıklanıldı")
            autopy.mouse.click()
    except:
        pass

def VolumeControl(lmList, bbox, img):
    h, w, c = img.shape
    wScr, hScr = autopy.screen.size()
    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    print(area)

    try:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        sonuc = m.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
        print("değer:",str(sonuc / area))
        if 0.001 < (sonuc / area) < 0.002:
            print("Ses artırılıyor")
            currentVolumeDb = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(currentVolumeDb + 0.3, None)

        elif 0.001 > (sonuc / area):
            print("Ses Azaltılıyor")
            currentVolumeDb = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(currentVolumeDb - 0.3, None)

    except:
        pass




def main():
    pTime = 0

    cap = cv2.VideoCapture(0)
    detector = hs.handDetector()
    while True:
        success, img = cap.read()
        h, w, c = img.shape
        wScr,hScr = autopy.screen.size()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)


        if len(lmList) != 0:
            MouseControl(lmList,bbox,img)
            VolumeControl(lmList,bbox,img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

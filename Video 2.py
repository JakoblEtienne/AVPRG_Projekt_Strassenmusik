import numpy as np
import cv2
import rtmidi
import mido
import time
import copy

#print("Midi output ports: ", mido.get_output_names())
midiOutput = mido.open_output("LoopBe Internal MIDI 1")

def sendNoteOn(note, velocity):
    message = mido.Message('note_on', note=note, velocity=velocity)
    midiOutput.send(message)

def sendNoteOff(note, velocity):
    message = mido.Message('note_off', note=note, velocity=velocity)
    midiOutput.send(message)

def sendControlChange(control, value):
    message = mido.Message('control_change', control=control, value=value)
    midiOutput.send(message)

cap = cv2.VideoCapture("Straße 2.mp4")

fgbg = cv2.createBackgroundSubtractorMOG2()

#disabling shadow-detection
fgbg.setShadowValue(0)

#kernel for morph_close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))


notePlaying1 = False
notePlaying2 = False
notePlaying3 = False
notePlaying4 = False
notePlaying5 = False
notePlaying6 = False

lastPlayedNote1 = None
lastPlayedNote2 = None
lastPlayedNote3 = None
lastPlayedNote4 = None
lastPlayedNote5 = None
lastPlayedNote6 = None

while cap.isOpened():
    ret, frame = cap.read()

    #grayscale of the original frame
    grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #average grayvalue of the pixels in the detection zones
    brightnessLane1 = int((np.mean(grayScale[100:105, 160:210]))/2)
    brightnessLane2 = int((np.mean(grayScale[100:105, 280:330]))/2)
    brightnessLane3 = int((np.mean(grayScale[100:105, 400:450]))/2)
    brightnessLane4 = int((np.mean(grayScale[100:105, 690:740]))/2)
    brightnessLane5 = int((np.mean(grayScale[100:105, 820:870]))/2)
    brightnessLane6 = int((np.mean(grayScale[100:105, 950:1000]))/2)

    #blurring the image to remove noise
    gaussianBlur = cv2.GaussianBlur(frame, (11,11), 0)

    fgmask = fgbg.apply(gaussianBlur, 0.5)

    #Medianfilter 5x5
    median = cv2.medianBlur(fgmask, 5)

    opening = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel)

    #needed average to detect a car
    neededAvg = 102

    #average of black and white pixels in the detection zones
    bwAvgLane1 = np.mean(opening[100:105, 160:210])
    bwAvgLane2 = np.mean(opening[100:105, 280:330])
    bwAvgLane3 = np.mean(opening[100:105, 400:450])
    bwAvgLane4 = np.mean(opening[100:105, 690:740])
    bwAvgLane5 = np.mean(opening[100:105, 820:870])
    bwAvgLane6 = np.mean(opening[100:105, 950:1000])


    #rectangles around the detection zones
    cv2.rectangle(frame, (160,100), (210,105), (0,255,0), 4)
    cv2.rectangle(frame, (280,100), (330,105), (0,255,0), 4)
    cv2.rectangle(frame, (400,100), (450,105), (0,255,0), 4)
    cv2.rectangle(frame, (690,100), (740,105), (0,255,0), 4)
    cv2.rectangle(frame, (820,100), (870,105), (0,255,0), 4)
    cv2.rectangle(frame, (950,100), (1000,105), (0,255,0), 4)

    #car detection 1st lane
    if bwAvgLane1 >= neededAvg and not notePlaying1:
        lastPlayedNote1 = copy.deepcopy(brightnessLane1)
        sendNoteOn(brightnessLane1,1)
        print(brightnessLane1)
        notePlaying1 = True
    elif bwAvgLane1 >= neededAvg and notePlaying1:
        pass
    elif bwAvgLane1 < neededAvg and notePlaying1:
        sendNoteOff(lastPlayedNote1,1)
        notePlaying1 = False
    else:
        pass
    
    #car detection 2nd lane
    if bwAvgLane2 >= neededAvg and not notePlaying2:
        lastPlayedNote2 = copy.deepcopy(brightnessLane2)
        sendNoteOn(brightnessLane2,2)
        print(brightnessLane2)

        notePlaying2 = True
    elif bwAvgLane2 >= neededAvg and notePlaying2:
        pass
    elif bwAvgLane2 < neededAvg and notePlaying2:
        sendNoteOff(lastPlayedNote2,2)
        notePlaying2 = False
    else:
        pass

    #car detection 3rd lane
    if bwAvgLane3 >= neededAvg and not notePlaying3:
        lastPlayedNote3 = copy.deepcopy(brightnessLane3)
        sendNoteOn(brightnessLane3,3)
        print(brightnessLane3)

        notePlaying3 = True
    elif bwAvgLane3 >= neededAvg and notePlaying3:
        pass
    elif bwAvgLane3 < neededAvg and notePlaying3:
        sendNoteOff(lastPlayedNote3,3)
        notePlaying3 = False
    else:
        pass

    #car detection 4th lane
    if bwAvgLane4 >= neededAvg and not notePlaying4:
        lastPlayedNote4 = copy.deepcopy(brightnessLane4)
        sendNoteOn(brightnessLane4,4)
        print(brightnessLane4)
        notePlaying4 = True
    elif bwAvgLane4 >= neededAvg and notePlaying4:
        pass
    elif bwAvgLane4 < neededAvg and notePlaying4:
        sendNoteOff(lastPlayedNote4,4)
        notePlaying4 = False
    else:
        pass
    
    #car detection 5th lane
    if bwAvgLane5 >= neededAvg and not notePlaying5:
        lastPlayedNote5 = copy.deepcopy(brightnessLane5)
        sendNoteOn(brightnessLane5,5)
        print(brightnessLane5)

        notePlaying5 = True
    elif bwAvgLane5 >= neededAvg and notePlaying5:
        pass
    elif bwAvgLane5 < neededAvg and notePlaying5:
        sendNoteOff(lastPlayedNote5,5)
        notePlaying5 = False
    else:
        pass

    #car detection 6th lane
    if bwAvgLane6 >= neededAvg and not notePlaying6:
        lastPlayedNote6 = copy.deepcopy(brightnessLane6)
        sendNoteOn(brightnessLane6,6)
        print(brightnessLane6)

        notePlaying6 = True
    elif bwAvgLane6 >= neededAvg and notePlaying6:
        pass
    elif bwAvgLane6 < neededAvg and notePlaying6:
        sendNoteOff(lastPlayedNote6,6)
        notePlaying6 = False
    else:
        pass

    #cv2.imshow("Mask", opening)
    #cv2.imshow("Blurred Image", gaussianBlur)
    cv2.imshow("Original", frame)

    if cv2.waitKey(25) != -1:
        break

cap.release()
cv2.destroyAllWindows()

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

cap = cv2.VideoCapture("Video3_24fps.mp4")

fgbg = cv2.createBackgroundSubtractorMOG2()

#disabling shadow-detection
fgbg.setShadowValue(0)

#kernel for morph_close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

framecount = 0

notePlayingLeft = False
notePlayingMiddle = False
notePlayingRight = False

lastPlayedNoteLeft = None
lastPlayedNoteMiddle = None
lastPlayedNoteRight = None

while cap.isOpened():
    ret, frame = cap.read()

    framecount += 1

    print(framecount)


    #grayscale of the original frame
    grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #average grayvalue of the pixels in the detection zones
    brightnessLaneLeft = int((np.mean(grayScale[800:850, 300:500]))/2)
    brightnessLaneMiddle = int((np.mean(grayScale[800:850, 850:1050]))/2)
    brightnessLaneRight = int((np.mean(grayScale[800:850, 1400:1600]))/2)

    #blurring the image to remove noise
    #gaussianBlur = cv2.GaussianBlur(frame, (11,11), 0)

    fgmask = fgbg.apply(frame, 0.5)

    #Medianfilter 5x5
    median = cv2.medianBlur(fgmask, 5)

    closing = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel)

    #needed average to detect a car
    neededAvg = 77 # =30/70 # 102=40/60

    #average of black and white pixels in the detection zones
    bwAvgLaneLeft = np.mean(closing[800:850, 300:500])
    bwAvgLaneMiddle = np.mean(closing[800:850, 850:1050])
    bwAvgLaneRight = np.mean(closing[800:850, 1400:1600])

    #rectangles around the detection zones
    cv2.rectangle(frame, (300,800), (500,850), (0,255,0), 4)
    cv2.rectangle(frame, (850,800), (1050,850), (0,255,0), 4)
    cv2.rectangle(frame, (1400,800), (1600,850), (0,255,0), 4)
   
    if np.mean(closing[800:850, 0:1920]) <= 80:

        #car detection left lane
        if bwAvgLaneLeft >= neededAvg and not notePlayingLeft:
            if lastPlayedNoteLeft != None:
                sendNoteOff(lastPlayedNoteLeft,5)
                print("extrastop left")
            lastPlayedNoteLeft = copy.deepcopy(brightnessLaneLeft)
            sendNoteOn(brightnessLaneLeft,5)
            print("note sent left")
            print("brightness total", np.mean(closing[800:850, 0:1920]))
            print("brightness left", bwAvgLaneLeft)
            notePlayingLeft = True
        elif bwAvgLaneLeft >= neededAvg and notePlayingLeft:
            pass
        elif bwAvgLaneLeft < neededAvg and notePlayingLeft:
            sendNoteOff(lastPlayedNoteLeft,5)
            notePlayingLeft = False
            print("note stopped left")
        else:
            pass
        
        #car detection middle lane
        if bwAvgLaneMiddle >= neededAvg and not notePlayingMiddle:
            if lastPlayedNoteMiddle != None:
                sendNoteOff(lastPlayedNoteMiddle,3)
                print("extrastop middle")
            lastPlayedNoteMiddle = copy.deepcopy(brightnessLaneMiddle)
            sendNoteOn(brightnessLaneMiddle,3)
            print("note sent middle")
            print("brightness total", np.mean(closing[800:850, 0:1920]))
            print("brightness middle", bwAvgLaneMiddle)
            notePlayingMiddle = True
        elif bwAvgLaneMiddle >= neededAvg and notePlayingMiddle:
            pass
        elif bwAvgLaneMiddle < neededAvg and notePlayingMiddle:
            sendNoteOff(lastPlayedNoteMiddle,3)
            notePlayingMiddle = False
            print("note stopped middle")
        else:
            pass

        #car detection right lane
        if bwAvgLaneRight >= neededAvg and not notePlayingRight:
            if lastPlayedNoteRight != None:
                sendNoteOff(lastPlayedNoteRight,1)
                print("extrastop right")
            lastPlayedNoteRight = copy.deepcopy(brightnessLaneRight)
            sendNoteOn(brightnessLaneRight,1)
            print("Note sent right")
            print("brightness total", np.mean(closing[800:850, 0:1920]))
            print("brightness Right", bwAvgLaneRight)
            notePlayingRight = True
        elif bwAvgLaneRight >= neededAvg and notePlayingRight:
            pass
        elif bwAvgLaneRight < neededAvg and notePlayingRight:
            sendNoteOff(lastPlayedNoteRight,1)
            notePlayingRight = False
            print("note stopped right")
        else:
            pass



    #cv2.imshow("Mask", closing)
    #cv2.imshow("Blurred Image", gaussianBlur)
    cv2.imshow("Original", frame)

    if cv2.waitKey(25) != -1:
        break

cap.release()
cv2.destroyAllWindows()

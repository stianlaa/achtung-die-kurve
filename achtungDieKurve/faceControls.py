from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
from common import PLAYERS, WIDTH, HEIGHT, PLAYER_COLORS

# parameters for loading data and images
detection_model_path = 'emotion/haarcascadeFrontalfaceDefault.xml'
emotion_model_path = 'emotion/_mini_XCEPTION.106-0.65.hdf5'

PLAYER_FRAME_WIDTH = round(WIDTH/PLAYERS)
PLAYER_FRAME_HEIGHT = HEIGHT

DISPLAY_SCREEN = False
FRAME_WIDTH = 4

face_detection =  cv2.CascadeClassifier(detection_model_path)

EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

camera = cv2.VideoCapture(0)
if DISPLAY_SCREEN:
    cv2.namedWindow('facecontrol')

def initializeFaceControlList():
    controlList = []
    for playerIndex in range(0, PLAYERS):
        controlList.append({"extractedEmotion": None, "turnDirection": None, "probability": 0})
    return controlList

playerEmotionControls = initializeFaceControlList()


# Check for most probable of the chosen emotions and neutral
def extractMostProbable(chosenEmotions, predictions):
    mostProbable = None
    maxProbability = 0
    for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, predictions)):
        if emotion in chosenEmotions:
            if mostProbable == None:
                mostProbable = emotion
                maxProbability = prob
            elif prob > maxProbability:
                mostProbable = emotion
                maxProbability = prob
    return {"mostProbable": mostProbable, "probability": maxProbability}


def getFaceControls(emotionControls, emotion_classifier):

    # starting video streaming
    frame = camera.read()[1]

    #Expensive operation, costly to enlarge
    frame = imutils.resize(frame, width=WIDTH) 
    canvas = np.zeros((HEIGHT, HEIGHT, 3), dtype="uint8")
    frameClone = frame.copy()
    preds = None
   
    for playerIndex in range(0, PLAYERS):
        lowerLeft = (PLAYER_FRAME_WIDTH*playerIndex + FRAME_WIDTH, FRAME_WIDTH)
        topRight = (PLAYER_FRAME_WIDTH*(playerIndex + 1) - FRAME_WIDTH, PLAYER_FRAME_HEIGHT - FRAME_WIDTH)
        if DISPLAY_SCREEN:
            cv2.rectangle(frameClone, lowerLeft, topRight, PLAYER_COLORS[playerIndex][::-1], FRAME_WIDTH)
        playerFrame = frameClone[lowerLeft[1]:topRight[1], lowerLeft[0] : topRight[0],:]
       
        gray = cv2.cvtColor(playerFrame, cv2.COLOR_BGR2GRAY)
       
        faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, 
            # and then prepare the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
            preds = emotion_classifier.predict(roi)[0]
            if preds is not None:
                extractedEmotion = extractMostProbable(list(emotionControls.keys()), preds)
                turnDirection = emotionControls[extractedEmotion["mostProbable"]]
                probability = extractedEmotion["probability"]
                playerEmotionControls[playerIndex] = {"extractedEmotion": extractedEmotion, "turnDirection": turnDirection, "probability": probability}
               
    if DISPLAY_SCREEN:
        cv2.imshow('facecontrol', frameClone)
   
    return playerEmotionControls

def faceControlLoop(controls):
    right = "angry"
    left = "happy"
    forward = "neutral"
    controlEmotions = {right: "RIGHT", left: "LEFT", forward: None}

    emotion_classifier = load_model(emotion_model_path, compile=False)

    while True:
        
        result = getFaceControls(controlEmotions, emotion_classifier)
        if result is not None and len(result) > 0:
            controls[:] = result
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()
 
# TODO: refactor and improve code greatly
# - perhaps a sensitivity rate adjuster, basically just multiplier constants to be set
#   for all of the emotions

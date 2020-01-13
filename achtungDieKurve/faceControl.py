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

FRAME_WIDTH = 4

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

def getEmotionControls():
    # starting video streaming
    cv2.namedWindow('your_face')
    camera = cv2.VideoCapture(0)
    while True:
        frame = camera.read()[1]

        #Expensive operation, costly to enlarge
        frame = imutils.resize(frame, width=WIDTH) 

        canvas = np.zeros((HEIGHT, HEIGHT, 3), dtype="uint8")
        frameClone = frame.copy()

        preds = None        
        for playerIndex in range(0, PLAYERS):
            lowerLeft = (PLAYER_FRAME_WIDTH*playerIndex + FRAME_WIDTH, FRAME_WIDTH)
            topRight = (PLAYER_FRAME_WIDTH*(playerIndex + 1) - FRAME_WIDTH, PLAYER_FRAME_HEIGHT - FRAME_WIDTH)
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
                emotion_probability = np.max(preds)
                label = EMOTIONS[preds.argmax()]

                if preds is not None:
                    for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                        #construct the label text
                        text = "{}: {:.2f}%".format(emotion, prob * 100)
                        w = int(prob * 300)
                        cv2.rectangle(frameClone, (lowerLeft[0] + 7, lowerLeft[1] + (i * 35) + 5), (lowerLeft[0] + w, lowerLeft[1] + (i * 35) + 35), PLAYER_COLORS[playerIndex][::-1], -1)
                        #cv2.putText(frameClone, text, (10, (i * 35) + 23),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                        cv2.putText(frameClone, label, (lowerLeft[0] + fX, lowerLeft[1] + fY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, PLAYER_COLORS[playerIndex][::-1], 2)
                        cv2.rectangle(frameClone, (lowerLeft[0] + fX, lowerLeft[1] + fY), (lowerLeft[0] + fX + fW, lowerLeft[1] + fY + fH), PLAYER_COLORS[playerIndex][::-1], 2)


        #############

        cv2.imshow('your_face', frameClone)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    getEmotionControls()
    camera.release()
    cv2.destroyAllWindows()

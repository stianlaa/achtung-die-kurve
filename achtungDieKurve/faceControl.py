from keras.preprocessing.image import img_to_array
import imutils
from common import PLAYERS, WIDTH, HEIGHT
import cv2
from keras.models import load_model
import numpy as np

# parameters for loading data and images
detection_model_path = 'emotion/haarcascadeFrontalfaceDefault.xml'
emotion_model_path = 'emotion/_mini_XCEPTION.106-0.65.hdf5'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

cv2.namedWindow('faces')
camera = cv2.VideoCapture(0)

def getEmotionControls():
    frame = camera.read()[1]
    cameraFrame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
    # cameraFrameClone = playerFrame.copy() # TODO initialize with zeroes instead?
    #constructedFrame = TODO: have to merge results and build new frame thingy

    for playerIndex in range(PLAYERS):
        playerFrame = cameraFrame[0:HEIGHT, round((playerIndex/PLAYERS)*WIDTH):round(((playerIndex + 1)/PLAYERS)*WIDTH)]
        gray = cv2.cvtColor(playerFrame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        playerCanvas = np.zeros((round(WIDTH/PLAYERS), HEIGHT, 3), dtype="uint8")

        preds = None
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
            # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
            # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            cv2.putText(cameraFrame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(cameraFrame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)

        # TODO: draw stripes between playercanvas
        # TODO: show probabilities for one specific player if active

        # if preds is not None and False:
            # for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                # construct the label text
                # text = "{}: {:.2f}%".format(emotion, prob * 100)
                # w = int(prob * 300)
                # cv2.rectangle(playerCanvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
                # cv2.putText(playerCanvas, text, (10, (i * 35) + 23),
                # cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                # cv2.putText(playerFrameClone, label, (fX, fY - 10),
                # cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                # cv2.rectangle(playerFrameClone, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
        
            
            # TODO: should probably place in destructor
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            camera.release()
            cv2.destroyAllWindows()
        
        cv2.imshow('your_face', cameraFrame)
        # TODO: replace with most probably emotion in each frame
        #cv2.imshow("Probabilities", playerCanvas)

        # TODO: convert emotions to control output

if __name__ == '__main__':
    while True:
        getEmotionControls()

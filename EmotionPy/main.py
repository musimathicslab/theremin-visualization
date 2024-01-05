from keras.models import load_model
from time import sleep
from keras.utils import img_to_array
from keras.preprocessing import image
from pythonosc import udp_client
import schedule

import cv2
import numpy as np


face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('EmotionDetectionModel.h5')
class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

IP = "192.168.1.10"
PORT = 7000
OSC_ADDRESS = "/emotion"
CAPTURE_INDEX = 1
SECONDS_INTERVAL = 1

client = udp_client.SimpleUDPClient(IP, PORT)

cap = cv2.VideoCapture(CAPTURE_INDEX)
label = "Neutral"
check_label = "Neutral"

def send_label(lbl = "Neutral"):
		check_label = label

		if check_label == label:
			client.send_message(OSC_ADDRESS, label)
			print("sent ", label, " to ", OSC_ADDRESS)

schedule.every(SECONDS_INTERVAL).seconds.do(send_label, lbl = label)

while True:
	schedule.run_pending()
	ret, frame = cap.read()
	
	if frame is None:
		continue

	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces=face_classifier.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray=gray[y:y+h,x:x+w]
		roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

		if np.sum([roi_gray])!=0:
			roi=roi_gray.astype('float')/255.0
			roi=img_to_array(roi)
			roi=np.expand_dims(roi,axis=0)
			preds=classifier.predict(roi)[0]
			label=class_labels[preds.argmax()]
			label_position=(x,y)
			cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
		else:
			cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)



	# cv2.imshow('Emotion Detector', frame)
	

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
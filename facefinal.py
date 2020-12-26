import numpy as np
import cv2
import time
import emotion_prediction

#import the cascade for face detection
face_cascade = cv2.CascadeClassifier('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\haarcascade_frontalface_default.xml')

def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)

    image_to_predict = []
    num = 0 
    while num<1:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # to detect faces in video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            image_to_predict = cropped_img
            cv2.imwrite('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\cropped_image_to_predict.jpg', roi_gray)



        cv2.imwrite('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\opencv'+str(num)+'.jpg',frame)
        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    emo=emotion_prediction.predict(image_to_predict)
    return emo


if __name__ == "__main__":
    TakeSnapshotAndSave()




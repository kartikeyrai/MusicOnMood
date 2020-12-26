
import combine
import sys
import cartoon
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import tensorflow as tf
import numpy as np
import os,glob,cv2
from os import walk,path
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

import sys,argparse


def emotion_detection_model():
    # Create the model
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))

    return model


def predict(cropped_image):
    curr_folder = path.dirname(path.realpath(__file__))

    photo='C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\opencv0.jpg'
    image_size=128
    num_channels=3
    images = []
    # Reading the image using OpenCV
    image = cv2.imread(photo)
    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size),0,0, cv2.INTER_LINEAR)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0/255.0)
    #The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
    x_batch = images.reshape(1, image_size,image_size,num_channels)

    model = emotion_detection_model()
    model.load_weights('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\model.h5')

    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    prediction = model.predict(cropped_image, steps=None)
    maxindex = int(np.argmax(prediction))
    predicted_emotion = emotion_dict[maxindex]

    cartoon.create()

    # print(predicted_emotion)



    return predicted_emotion

if __name__ == "__main__":
    predict()

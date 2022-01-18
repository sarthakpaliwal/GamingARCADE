'''
Squeezenet Neural network used
Few new layes added to accomodate new classes (Rock paper scissors none)

'''
import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os

#points to directory where images are stored
IMG_SAVE_PATH = 'image_data' 

#class map dict defined  converteing label to number for easier code
CLASS_MAP = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "none": 3
} 
#number of classess= length of classmap=4 

NUM_CLASSES = len(CLASS_MAP)

#takes in a value and pas it to value in class map mapper(rock)=0
def mapper(val):
    return CLASS_MAP[val]

#layers added onto the squeezenet network
def get_model():
    model = Sequential([ #in the first laye pass the entire squeezenet model itself
        SqueezeNet(input_shape=(227, 227, 3), include_top=False), #image is 227*227 in size with RGB as 3 channels
        Dropout(0.5), #to provide overfitting 50% dropout rate
        Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),#2dConvoultional layer with number of classes
        Activation('relu'),#rectified linear unit
        GlobalAveragePooling2D(),# classification with average output of each feature map in the previous layer (data reduction)
        Activation('softmax') #softmax to get the probablities  of each gesture
    ])
    return model


# load images from the directory to train
dataset = [] #traveres the directory in which imges saved
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item)) #load images into directory
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert from BGR to RGB for training
        img = cv2.resize(img, (227, 227))#image resize for squeezenet 
        dataset.append([img, directory]) #label formed as below

'''
dataset = [
    [[...], 'rock'], entire image array with gesture it represnets
    [[...], 'paper'], unpack dataset list to to get data/ fetures in one arryaa and corresponding labels in another array
    ...
]
'''
data, labels = zip(*dataset) #data unpack 
labels = list(map(mapper, labels))


'''
labels: rock,paper,paper,scissors,rock...
one hot encoded: [1,0,0], [0,1,0], [0,1,0], [0,0,1], [1,0,0]...
'''

# one hot encode the labels
labels = np_utils.to_categorical(labels)

# define the model
model = get_model()
model.compile(
    optimizer=Adam(lr=0.0001),#adam with learning rate as 0.0001 as defaut doesnt suit
    loss='categorical_crossentropy',#since classification
    metrics=['accuracy'] #to record
)

# start training
model.fit(np.array(data), np.array(labels), epochs=10)

# save the model for later use on current directory and local machine
model.save("rock-paper-scissors-model.h5")

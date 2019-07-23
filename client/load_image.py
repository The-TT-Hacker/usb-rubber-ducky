import pickle
import cv2

#image = pickle.load("data/web_cam1")

file = open('data/web_cam1', 'r')
image = file.read()

image.encode()

print(image)

cv2.imshow('ImageWindow', image)
cv2.waitKey()
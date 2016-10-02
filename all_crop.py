from PIL import Image
import urllib
import json
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import urllib
import Image

#Reading the sample link url
response = urllib.urlopen("https://test.flaunt.peekabuy.com/api/board/get_jc_product_images_batch/?page=2")
json_1=response.read()

#Function to convert json into appropriate data suitable for processing
def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data
    
diction_1=convert(json_1)
d=json.loads(diction_1)

#List of list of images with urls stored at the first position in every list. (0th index)
images_urls=list(d["images"])

#Processes every image in 300 sample images and displays the cropped image with the original image.
for i in range(len(images_urls)):
	urllib.urlretrieve(images_urls[i][0], "test_image.JPEG")
	original = cv2.imread('test_image.JPEG')
	cv2.imshow("Original image",original)
	img=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)

    # Calculate the gradient image, for example using Sobel operator
	# Output dtype = cv2.CV_64F. Then take its absolute and convert to cv2.CV_8U
	sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
	abs_sobel64f = np.absolute(sobelx64f)
	sobel_8u = np.uint8(abs_sobel64f)

	# Find the possible contours in the image to locate the object
	contours,hierarchy = cv2.findContours(sobel_8u,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	# Find the index of the contour with maximum area
	areas = [cv2.contourArea(c) for c in contours]

	max_index = np.argmax(areas)
	cnt=contours[max_index]

	## Draw a bounding box around the largest contour representing the object to be cropped.
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(original,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.imshow("Cropping result",original)

	cv2.waitKey()
	cv2.destroyAllWindows()

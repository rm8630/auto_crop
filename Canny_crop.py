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

#Processes every image in 300 sample images and displays the cropped image with the original image
for i in range(len(images_urls)):
	urllib.urlretrieve(images_urls[i][0], "test_image.JPEG")
	original = cv2.imread('test_image.JPEG')
	cv2.imshow("Original image",original)
	img=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
	
	#Calculates the Canny edges
        edges=cv2.Canny(img,100,200)

	# Calculates the co-ordinates of the bounding box 
	cord=np.argwhere(edges==255)
	y_min=min(cord[:,0])-5
	y_max=max(cord[:,0])+30
	x_min=min(cord[:,1])-5
	x_max=max(cord[:,1])+5

	##Drawing the bounding box around the object
	cv2.rectangle(original,(x_min,y_min),(x_max,y_max),(0,255,0),2)
	cv2.imshow("Cropping result",original)
	cv2.waitKey()
	cv2.destroyAllWindows()



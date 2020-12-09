import numpy as np
import cv2
import glob, os
import re
import matplotlib.pyplot as plt
from tkinter import Tk 
from tkinter.filedialog import askopenfilename

img_w = 75
img_h = 75

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, filename):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	# s = ssim(imageA, imageB)
	# setup the figure
	print("%s - MSE: %.2f" % (filename, m))
	if m == 0:
		print("\nThe input image is %s" % (re.findall('\d+', filename))[0])
		return (re.findall('\d+', filename))[0]
	else:
		return 0
	
puzzle = np.ones((225,225,3))

img_num = input("Start? (y/n) ")

while str(img_num) != 'n' :

	try:
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
		filename = askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")]) # show an "Open" dialog box and return the path to the selected file
		print(filename)
		input_img = cv2.imread(filename)
		input_img = cv2.resize(input_img, (img_w, img_h), interpolation=cv2.INTER_AREA)

	except :
		print ("\nNo file selected.\n")
		img_num = input("Continue? (y/n) ")
		continue
		
	input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

	folder = '/Users/zhejing/Puzzle/CROP/*.png'
	num = 0
	for data_img in glob.glob(folder):
		filename = os.path.basename(data_img)
		data_img = cv2.imread(data_img)
		data_img = cv2.cvtColor(data_img, cv2.COLOR_BGR2RGB)
		num = int(compare_images(input_img, data_img, filename))
		y = ((num-1) // 3) * img_h
		x = ((num-1) % 3) * img_w
		print(x, y)

		if num:
			puzzle[y:y+img_h, x:x+img_w] = input_img
			break

	if not num:
		print("\nNo such part in your puzzle!")

	img_num = input("Continue? (y/n) ")

plt.axis('off')
plt.imshow(puzzle.astype('uint8'))
plt.show()




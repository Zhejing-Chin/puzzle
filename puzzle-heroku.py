import numpy as np
import cv2
import glob, os
import streamlit as st
import io
from PIL import Image
import tensorflow as tf


st.set_option('deprecation.showfileUploaderEncoding', False)

st.write("""
# Auto Puzzle App
This app assembles the puzzle parts. 
""")


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

uploaded_file = st.file_uploader("Upload a file", type=("png", "jpg"))

@st.cache(suppress_st_warning=True)
def output():
	if uploaded_file == None:
		st.warning('No file selected.')
	else:
		filename = uploaded_file.read()
		input_img = Image.open(io.BytesIO(filename))
		input_img = input_img.resize((img_w, img_h), Image.LANCZOS)
		input_img = tf.keras.preprocessing.image.img_to_array(input_img)

		folder = 'CROP/*.png'
		num = 0
		for data_img in glob.glob(folder):
			filename = os.path.basename(data_img)
			data_img = cv2.imread(data_img)
			data_img = cv2.cvtColor(data_img, cv2.COLOR_BGR2RGB)
			num = int(compare_images(input_img, data_img, filename))
			y = ((num-1) // 3) * img_h
			x = ((num-1) % 3) * img_w

			if num:
				puzzle[y:y+img_h, x:x+img_w] = input_img
				break

		if not num:
			st.write("\nNo such part in your puzzle!")

	return puzzle.astype('uint8')

st.write("""Your Puzzle """)
st.image(output(), clamp=True, use_column_width=True)





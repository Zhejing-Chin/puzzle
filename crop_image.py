import cv2, time
from PIL import Image 
import matplotlib.pyplot as plt

img_w = 225
img_h = 225
pcs = int(img_w / 3)

image_path = '/Users/zhejing/Puzzle/20200530_184414.jpg'

im = cv2.imread(image_path)
im_resized = cv2.resize(im, (img_w, img_h), interpolation=cv2.INTER_AREA)
img = cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGB)

image_data = []

y = 0
while y < img_h:
	x = 0
	image_data.append(img[y: y+pcs, x: x+pcs])
	cv2.imwrite("CROP/"+str(len(image_data))+".png", 
		cv2.cvtColor(img[y: y+pcs, x: x+pcs], cv2.COLOR_RGB2BGR))
	x+=pcs
	while x < img_w:
		image_data.append(img[y: y+pcs, x: x+pcs])
		cv2.imwrite("CROP/"+str(len(image_data))+".png", 
			cv2.cvtColor(img[y: y+pcs, x: x+pcs], cv2.COLOR_RGB2BGR))
		x+=pcs
	y+=pcs

for num, part in enumerate(image_data):
	plt.subplot(3, 3, num+1)
	plt.axis('off')
	plt.imshow(part, aspect='auto')

plt.subplots_adjust(hspace=0.01, wspace=0.01)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

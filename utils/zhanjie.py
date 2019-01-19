import cv2
import numpy as np
import skimage

cover_color = [60, 64, 37] # bgr
cover_alpha = 0.85
noise_alpha = 0.7

def downsample(image, height, width, iter=2):
	for i in range(iter):
		height = height // 2
		width = width // 2
		image = cv2.resize(image, dsize=(width, height), interpolation=cv2.INTER_LINEAR)
		height = height * 2
		width = width *  2
		image = cv2.resize(image, dsize=(width, height), interpolation=cv2.INTER_LINEAR)
		
	return image
	
def add_noise(in_image):
	return skimage.util.random_noise(in_image, mode='gaussian', var=0.001)

	
def pre_process(in_image):
	# shorter = 500
	height, width = in_image.shape[0:2]
	if width > height:
		width = int(width / (height / 500.0))
		height = 500
		return cv2.resize(in_image, dsize=(width, height))
	else:
		height = int(height / (width / 500.0))
		width = 500
		return cv2.resize(in_image, dsize=(width, height))
	
def contrast_and_light(in_image, alpha, beta):
	res = np.uint8(np.clip(alpha * in_image + beta, 0, 255))
	return res
	
def mask_screen_noise(in_image, choose=0):
	noise_list = ['./noise_1.jpg', './noise_2.jpg', './noise_3.jpg']
	noise_image = cv2.imread(noise_list[choose])
	if in_image.shape[0] > in_image.shape[1]:
		noise_image = np.transpose(noise_image, (1, 0, 2))
	
	noise_image = cv2.resize(noise_image, dsize=(in_image.shape[1], in_image.shape[0]))
	return np.uint8(in_image * noise_alpha + (1-noise_alpha) * noise_image)
	
def mask_icon(in_image, zoom_icon, glass_icon):
	# height = 500
	height, width = in_image.shape[0:2]
	if width <= height:
		glass_icon = np.transpose(glass_icon, (1, 0, 2))
		glass_icon = np.flip(glass_icon, 1)
	
	alpha_map = zoom_icon[:, :, 3]
	alpha_map = alpha_map[:, :, np.newaxis]
	alpha_map = np.repeat(alpha_map, repeats=3, axis=2) / 255.0
	
	glass_alpha = glass_icon[:, :, 3]
	glass_alpha = glass_alpha[:, :, np.newaxis]
	glass_alpha = np.repeat(glass_alpha, repeats=3, axis=2) / 255.0
	
	zoom_height, zoom_width = zoom_icon.shape[0:2]
	glass_height, glass_width = glass_icon.shape[0:2]
	
	if width > height:
		# right bottom
		in_image[350:350+zoom_height, width-200:width-200+zoom_width, :] = zoom_icon[:, :, 0:3] * alpha_map + (1.0-alpha_map)*in_image[350:350+zoom_height, width-200:width-200+zoom_width, :]
		in_image[420:420+glass_height, width-200:width-200+glass_width, :] = glass_icon[:, :, 0:3]*glass_alpha + (1.0-glass_alpha) * in_image[420:420+glass_height, width-200:width-200+glass_width, :]
	else:
		
		in_image[height-120:height-120+glass_height, 40:40+glass_width, :] = glass_icon[:,:,0:3]*glass_alpha + (1.0-glass_alpha)*in_image[height-120:height-120+glass_height, 40:40+glass_width, :]
		in_image[height-100:height-100+zoom_height, 45+glass_width:45+glass_width+zoom_width, :] = \
			zoom_icon[:, :, 0:3]*alpha_map + (1.0-alpha_map)*in_image[height-100:height-100+zoom_height, 45+glass_width:45+glass_width+zoom_width, :]
		
	return in_image
		

def zhanjie(in_image):
	zoom_icon = cv2.imread("./zoom.png", -1)
	glass_icon = cv2.imread("./glass.png", -1)
	zoom_icon = cv2.resize(zoom_icon, dsize=(90, 60))
	glass_icon = cv2.resize(glass_icon, dsize=(90, 45))

	in_image = pre_process(in_image)
	height, width = in_image.shape[0:2]
	in_image = downsample(in_image, height, width, iter=1)

	cover_image = np.zeros_like(in_image)
	cover_image[:, :, :] = cover_color

	in_image = mask_screen_noise(in_image, choose=0)
	in_image = np.uint8(in_image * cover_alpha + cover_image * (1-cover_alpha))
	in_image = contrast_and_light(in_image, 1.5, -30)
	in_image = mask_icon(in_image, zoom_icon, glass_icon)
	# cv2.imwrite("out2.jpg", in_image)
	return in_image

#in_image = cv2.imread("./test2.jpg")
#zoom_icon = cv2.imread("./zoom.png", -1)
#glass_icon = cv2.imread("./glass.png", -1)
#zoom_icon = cv2.resize(zoom_icon, dsize=(90, 60))
#glass_icon = cv2.resize(glass_icon, dsize=(90, 45))
#
#in_image = pre_process(in_image)
#
#height, width = in_image.shape[0:2]
#in_image = downsample(in_image, height, width, iter=1)
#
#
#cover_image = np.zeros_like(in_image)
#cover_image[:, :, :] = cover_color
## in_image = add_noise(in_image)
#in_image = mask_screen_noise(in_image, choose=0)
#in_image = np.uint8(in_image * cover_alpha + cover_image * (1-cover_alpha))
#in_image = contrast_and_light(in_image, 1.5, -30)
#in_image = mask_icon(in_image, zoom_icon, glass_icon)
#
#print(in_image.shape)
#print(zoom_icon.shape)
#print(glass_icon.shape)
#
##cv2.imshow("in_image", in_image)
##cv2.waitKey(0)
#cv2.imwrite("out.jpg", in_image)
#
if __name__ == '__main__':
	in_image = cv2.imread("./test2.jpg")
	zhanjie(in_image)

import cv2
import numpy as np
import os
import imutils
import pytesseract

suduku_arr = [[0 for _ in range(9)] for _ in range(9)]


def detect_entire_block(filename):
	img=cv2.imread(filename,0)
	edges=cv2.Canny(img,100,200)
	cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

	screenCnt = None
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.015 * peri, True)
		if len(approx) == 4:
			screenCnt = approx
			break
	x,y,w,h = cv2.boundingRect(screenCnt)
	crop_img = img[y:y+h,x:x+w]

	get_sep_block(crop_img, True)


def get_sep_block(img, itter, prefix=None):
	height, width = img.shape[:2]
	x = 0
	y = 0
	h = height // 3
	w = width // 3
	for i in range(3):
		for j in range(3):
			crop_img = img[y:y+h,x:x+w]
			offset = 8
			height, width = crop_img.shape[:2]
			crop_img = crop_img[offset:height-offset, offset:width-offset]
			if itter:
				new_file = "cv_"+str(prefix)+"_"+str(i)+str(j)+"_1.png"
			else:
				new_file = "cv_"+str(prefix)+"_"+str(i)+str(j)+"_0.png"

			if itter:
				get_sep_block(crop_img, False, prefix=str(i)+str(j))
			else:
				block_x = int(prefix)//10 * 3 + i
				block_y = int(prefix)%10 * 3 + j
				get_value_from_img(crop_img, block_x, block_y)

			x += w
		x = 0
		y += h

def get_value_from_img(img, x, y):
	text = pytesseract.image_to_string(img, lang='eng',
			config='--psm 6 -c tessedit_char_whitelist=0123456789').strip()
	if not text:
		text = "0"
	suduku_arr[x][y] = int(text)


if __name__ == "__main__":
	detect_entire_block('images/sudoku_01.jpg')

	for i in suduku_arr:
		print(i)

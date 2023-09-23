
import os
import traceback
import numpy as np
import cv2 
import imutils
from imutils import contours
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

for file in os.listdir("C:\\Users\\dell\\Desktop\\Pics\\"):
    print('Iam here ...')
    if file.endswith(".png"):
        file_path = "C:\\Users\\dell\\Desktop\\Pics\\" + str(file)
        print(file_path)
        img = cv2.imread(file_path)
        ratio = img.shape[0]/500.0
        original_img = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(img, (5,5) ,0)
        edged = cv2.Canny(gray, 75, 200)

        thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]


        #(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(gray, cnts, -1, (240, 0, 159), 3)

        H,W = img.shape[:2]
        for cnt in cnts:
            x,y,w,h = cv2.boundingRect(cnt)
            if cv2.contourArea(cnt) > 100 and (0.7 < w/h < 1.3) and (W/4 < x + w//2 < W*3/4) and (H/4 < y + h//2 < H*3/4):
                break


        mask = np.zeros(img.shape[:2],np.uint8)
        cv2.drawContours(mask, [cnt],-1, 255, -1)
        dst = cv2.bitwise_and(img, img, mask=mask)

        # displaying image and saving in the directory
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        scanned_file_name = "C:\\Users\\dell\\Desktop\\Pics\\" + str(file[:-4]) + "-Scanned.png" 
        cv2.imwrite(scanned_file_name, dst)
        cv2.imshow("gray.png", dst)
        cv2.waitKey()

        # fetching text from the image and storing it into a text file
        file_text = pytesseract.image_to_string(Image.open(scanned_file_name))
        print(file_text)
        text_file_name = "C:\\Users\\dell\\Desktop\\Pics\\" + str(file[:-4]) + "-Scanned.txt" 
        with open(text_file_name, "a") as f:
            f.write(file_text + "\n")
        # import pdb; pdb.set_trace()


import cv2
import numpy as np
import math

img = cv2.imread('test.jpg')
blur = cv2.GaussianBlur(img, (3,3), 0)
sat = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)[:,:,1]
thresh = cv2.threshold(sat, 50, 255, cv2.THRESH_BINARY)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
mask = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
cv2.imwrite("circuit_board_mask.png", mask)
cv2.imwrite("cleaned.png", otsu)
cv2.imshow("OTSU", otsu)

im = otsu
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.blur(imgray,(15,15))
ret,thresh = cv2.threshold(imgray,math.floor(np.average(imgray)),255,cv2.THRESH_BINARY_INV)
dilated=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)))
_,contours,_ = cv2.findContours(dilated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# edges = cv2.Canny(otsu, 50, 150, apertureSize=3)
# lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
# for r_theta in lines:
#     arr = np.array(r_theta[0], dtype=np.float64)
#     r, theta = arr
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*r
#     y0 = b*r
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#     cv2.line(otsu, (x1, y1), (x2, y2), (0, 0, 255), 2)
# cv2.imshow("lines", otsu)
# cv2.waitKey(0)
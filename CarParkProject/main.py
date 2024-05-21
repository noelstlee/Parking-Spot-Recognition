import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):
    for pos in posList:
        x,y = pos
        # cropping images for each parking space
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop) # distribution of distinct name for cropped images
        # need to count the number of pixels (lot of pixels -> there is a car!)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x,y+height - 3), scale = 1.2, thickness= 1, offset= 0)

        if count < 800: # vacant parking spot
            color = (0,255,0)
            thickness = 5
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

while True:
    # process for looping the video
    # check current pos = total number of frames present in video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # resetting the frames if they reach the total amount frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # convert into binary image
    # adaptive thresholding
    imgThreshhold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # for filtering out salt and pepper noise from the image above, use Median.
    imgMedian = cv2.medianBlur(imgThreshhold, 5)
    # making the pixels thicker. Using Dilation
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, None, iterations=1)
    checkParkingSpace(imgDilate)
    # note that we are drawing the rectangle after cropping since we don't want cropped images to have rectangles
    # for pos in posList:
    #    cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThresh", imgThreshhold)
    cv2.imshow("ImageMedian", imgMedian)
    # cv2.imshow("ImageDilate", imgDilate)
    cv2.waitKey(10) # slow the video a bit down



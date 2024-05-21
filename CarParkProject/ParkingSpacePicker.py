import cv2
import pickle

width, height = 107, 48

try:
    # if a file exists and contains a valid pickled data, 'pickle.load(f)' is used to deserilize the data
    # and load it into the variable 'posList'
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i) # remove that square position from posList
    # reads a pickled object from the open file f and returns it
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # we need to read the image again if it is not a video.
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
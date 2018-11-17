# import deque for our movement buffer
from collections import deque
import numpy as np
import math, cv2

# init the current frame of the video as well
# as a list of ROI points and a bool to determine
# whether or not we are in input mode
frame = None
roiPts = []
inputMode = False
pts = deque(maxlen=16)
depth = 12
mindiff = 7

# event triggered on mouse action
def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode
 
    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 8, (0, 255, 0), 2)
        cv2.imshow("frame", frame)

def getRotatedRectMidpoint(((x, y), (width, height), angle)):
  angle_rad = angle * math.pi / 180
  cosa = math.cos(angle_rad)
  sina = math.sin(angle_rad)
  wp = width/20
  hp = height/20
  return (x + wp * cosa - hp * sina,
          y + wp * sina + hp * cosa)

def main():

  global frame, roiPts, inputMode, pts

  camera = cv2.VideoCapture(0)

  cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
  cv2.setMouseCallback("frame", selectROI)

  termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
  roiBox = None

  while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    # check if we have reached the end of a video
    if not grabbed:
      break

    # if an roiBox has been computed
    if roiBox is not None:
      # convert the current frame to HSV color space
      # and perform mean shift
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

      # apply cam shift to the back projection, convert the
      # points to a bounding box, and draw them
      (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
      bpts = np.int0(cv2.boxPoints(r))
      (center, radius) = cv2.minEnclosingCircle(bpts)
      cv2.circle(frame, (int(round(center[0])), int(round(center[1]))), 4, (0, 255, 0), 2)
      cv2.polylines(frame, [bpts], True, (0, 255, 0), 2)
      cv2.ellipse(frame, r, (0, 0, 255), 2)
      # add the most recent point to the deque
      pts.appendleft((int(center[0]), int(center[1])))
      if len(pts) >= depth:
        dx = pts[-depth][0] - pts[1][0]
        dy = pts[-depth][1] - pts[1][1]
        cv2.putText(frame, "dx: " + str(dx), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dy: " + str(dy), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
        dirx = 0
        diry = 0
        if np.abs(dx) >= mindiff:
          dirx = np.sign(dx)
        if np.abs(dy) >= mindiff:
          diry = np.sign(dy)
        if dirx != 0 and diry != 0:
          if np.abs(dx) > np.abs(dy):
            diry = 0
          else:
            dirx = 0

        if dirx < 0:
          direction = 3
        elif dirx > 0:
          direction = 1
        elif diry < 0:
          direction = 2
        elif diry > 0:
          direction = 0
        else:
          direction = 4

        if (cv2.waitKey(1) == 32):
          print "spacebar pressed"
          # can send a special command here and a default command in an associated else branch
          cv2.putText(frame, "OVERRIDE", (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
              0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dir: " + str(direction), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
    
    for i in np.arange(1, len(pts)):
      if pts[i - 1] is None or pts[i] is None:
        continue

      cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 2)

    # show the frame and record if the user presses a key
    cv2.imshow("frame", frame)
    key = cv2.waitKey(7) & 0xFF
 
    # handle if the 'i' key is pressed, then go into ROI
    # selection mode
    if key == ord("i") and len(roiPts) < 4:
      # clear the roi points if we already had old ones
      # indicate that we are in input mode and clone the
      # frame
      inputMode = True
      orig = frame.copy()
   
      # keep looping until 4 reference ROI points have
      # been selected; press any key to exit ROI selction
      # mode once 4 points have been selected
      while len(roiPts) < 4:
          cv2.imshow("frame", frame)
          cv2.waitKey(0)
   
      # determine the top-left and bottom-right points
      roiPts = np.array(roiPts)
      s = roiPts.sum(axis = 1)
      tl = roiPts[np.argmin(s)]
      br = roiPts[np.argmax(s)]
   
      # grab the ROI for the bounding box and convert it
      # to the HSV color space
      roi = orig[tl[1]:br[1], tl[0]:br[0]]
      roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
      #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
   
      # compute a HSV histogram for the ROI and store the
      # bounding box
      roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
      roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
      roiBox = (tl[0], tl[1], br[0], br[1])
 
    # if the 'q' key is pressed, stop the loop
    elif key == ord("q"):
      break

  # cleanup the camera and close any open windows
  camera.release()
  cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()

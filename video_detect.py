import cv2
import numpy

# Open Web camera
cap = cv2.VideoCapture('GOPR1142.MP4')

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Hue saturation - 0..10 is a Redish color
center_hue = 13/2
low_H = center_hue - 7
high_H = center_hue + 7

# Saturation range - 100-255 is mid to saturated color
low_S = 0
high_S = 255

# Value(Brightness) range - 100-255 is mid to bright color
low_V = 0
high_V = 255

# Show image or Threshold
show_image = True

# Minumum size of the contour we search
min_contour_size = 150

# Settings for the overlay of rectangles
rectangle_thickness = 2
green = (0,255,0)
blue = (0,0,255)

# Settings for the hotkey text
font = cv2.FONT_HERSHEY_PLAIN
text_position = (10,10)
text_size = 1
text_color = (255, 255, 255)
hotkeys = 'Escape - Exit, Space - Image/Threshold, 1 - Decrease Countour Size, 2 - Increase Countour Size'

# Name my window
window_name = 'Output'
cv2.namedWindow(window_name)

# Skip to part with the gate
start_frame_number = 600
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)

while True:


    # Grab image from webcamera
    ret, frame = cap.read()

    if not ret:
        continue

    # Convert the image from BGR to HSV space
    # Cite: https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a threshold image

    # Cite: https://github.com/opencv/opencv/blob/master/samples/cpp/squares.cpp
    threshold = cv2.inRange(hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))

    # Using threshold calcuate countour data structure
    # Cite : https://docs.opencv.org/4.5.3/d4/d73/tutorial_py_contours_begin.html
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # For all objects in counters
    for item in range(len(contours)):
        cnt = contours[item]

        # Make sure object is big enough
        if len(cnt)<min_contour_size:
            continue

        # This eliminates detecting the reflection
        # approximate contour with accuracy proportional to the contour perimeter
        # Cite : https://docs.opencv.org/4.5.3/d4/d73/tutorial_py_contours_begin.html
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) > 4:
            # Not square/rectangle
            continue

        # Find bounding box of contour
        x,y,w,h = cv2.boundingRect(cnt)

        # Draw rectangle on the frame
        cv2.rectangle(frame,(x,y),(x+w,y+h),green, rectangle_thickness)

        # Calculate the rotated rectangle
        # Cite: https://newbedev.com/opencv-python-draw-minarearect-rotatedrect-not-implemented
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        # convert to integer coordinates
        box = numpy.int0(box)
        # Draw the rotated rectagle
        cv2.drawContours(frame,[box],0, blue, rectangle_thickness)

    # Show image or threshold
    if not show_image:
        frame = threshold

    # Draw text to show hot keys
    cv2.putText(frame, hotkeys, text_position, font, text_size, text_color, 1, cv2.LINE_AA)

    # Show the final image
    cv2.imshow(window_name, frame)

    # Grab which key is pressed
    key_pressed = cv2.waitKey(1)
    # Pressed Escape => exit
    if key_pressed == 27:
        break
    # Pressed spacebar => switch between showing Image vs Threshold
    elif key_pressed == ord(' '):
        show_image = not show_image
    # Pressed 1 => small countour size
    elif key_pressed == ord('1'):
        min_contour_size -= 10
        # Make sure its not too small
        min_contour_size = max(min_contour_size, 5)
    # Pressed 2 => medium countour size
    elif key_pressed == ord('2'):
        min_contour_size += 10



# Cleanup
cap.release()
cv2.destroyAllWindows()

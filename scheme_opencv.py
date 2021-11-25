import cv2
import numpy
from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

def add_opencv_special_forms(SPECIAL_FORMS):
    SPECIAL_FORMS["cv2.videocapture"] = do_cv2_videocapture_form
    SPECIAL_FORMS["cv2.imshow"] = do_cv2_imshow_form
    SPECIAL_FORMS["cv2.cvtcolor"] = do_cv2_cvtcolor_form
    SPECIAL_FORMS["cv2.inrange"] = do_cv2_inrange_form
    SPECIAL_FORMS["draw_contours"] = do_draw_contours_form

class MatProcedure(LambdaProcedure):
    """An OpenCV class defined by a lambda expression"""

    def __init__(self, mat, env):
        """A OpenCV Mat procedure"""
        assert isinstance(env, Frame), "env must be of type Frame"
        self.env = env
        self.mat = mat

    def __str__(self):
        return str(Pair('cv2.mat', Pair(self.mat, nil)))

    def __repr__(self):
        return 'MatProcedure({0}, {2})'.format(
            repr(self.mat), repr(self.env))

    def scheme_apply(self, method, env):
        validate_type(arg, lambda x: scheme_stringp(x), 0, 'MatProcedure')

        if(method == "size"):
            return self.mat.size

        raise SchemeError('unknown method call: {0}.{1}'.format(type(self), method))


class VideoCaptureProcedure(LambdaProcedure):
    """An OpenCV class defined by a lambda expression."""

    def __init__(self, arg, env):
        """A OpenCV videocapture procedure with arg"""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(arg, lambda x: scheme_numberp(x) or scheme_stringp(x), 0, 'VideoCaptureProcedure')

        # Not sure why strings have quotes around them, strip them
        if scheme_stringp(arg):
            arg = arg.strip('\"')
            arg = arg.strip("\'")

        self.arg = arg
        self.env = env

        self.cap = cv2.VideoCapture(self.arg)

    def __str__(self):
        return str(Pair('cv2.videocapture', Pair(self.arg, nil)))

    def __repr__(self):
        return 'VideoCaptureProcedure({0}, {2})'.format(
            repr(self.arg), repr(self.env))

    def scheme_apply(self, method, env):
        if(method.first == "read"):
            validate_form(method, 1)
            ret, frame = self.cap.read()
            return MatProcedure(frame, env)

        if(method.first == "set"):
            validate_form(method, 3)
            name = method.rest.first
            value = method.rest.rest.first
            if name == 'cv2.CAP_PROP_POS_FRAMES'.lower():
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, value)
            return

        raise SchemeError('unknown method call: {0}.{1}'.format(type(self), method.first))



def do_cv2_videocapture_form(expressions, env):
    """Evaluate an OpenCV VideoCapture form."""
    validate_form(expressions, 1)
    return VideoCaptureProcedure(expressions.first, env)


def do_cv2_imshow_form(expressions, env):
    """Evaluate an OpenCV image show form."""
    validate_form(expressions, 2)
    window_name = expressions.first
    if not isinstance(window_name, str):
        raise SchemeError('first argument should be string not', type(window_name), window_name)
    mat_name = expressions.rest.first
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('second argument should be matrix', type(mat_procedure), mat_procedure)

    frame = mat_procedure.mat

    # sometimes the image was invalid, so ignore it
    if type(frame) == type(None):
        return

    # side effect to show the image
    cv2.imshow(window_name, frame)

    # Need to wait key otherwise window will now show up
    cv2.waitKey(1)


def do_cv2_cvtcolor_form(expressions, env):
    """Applies cvtColor filter"""
    validate_form(expressions, 2)
    mat_name = expressions.first
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('first argument should be matrix', type(mat_procedure), mat_procedure)
    frame = mat_procedure.mat
    if type(frame) == type(None):
        return
    color_space = expressions.rest.first.rest.first
    #print(color_space, type(color_space))
    if color_space == "cv2.COLOR_BGR2HSV".lower():
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return MatProcedure(frame, env)


def do_cv2_inrange_form(expressions, env):
    """Applies inRange filter"""
    validate_form(expressions, 7)
    mat_name = expressions.first
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('first argument should be matrix', type(mat_procedure), mat_procedure)
    frame = mat_procedure.mat
    if type(frame) == type(None):
        return
    values = []
    while expressions.rest:
        x = expressions.rest.first
        values.append(expressions.rest.first)
        expressions = expressions.rest
    frame = cv2.inRange(frame, tuple(values[:3]), tuple(values[3:]))
    return MatProcedure(frame, env)


def do_draw_contours_form(expressions, env):
    """Applies inRange filter"""
    validate_form(expressions, 2)
    mat_name = expressions.first
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('first argument should be matrix', type(mat_procedure), mat_procedure)
    threshold = mat_procedure.mat
    if type(threshold) == type(None):
        return
    mat_name = expressions.rest.first
    mat_procedure = scheme_eval(mat_name, env)
    if not isinstance(mat_procedure, MatProcedure):
        raise SchemeError('first argument should be matrix', type(mat_procedure), mat_procedure)
    frame = mat_procedure.mat
    if type(frame) == type(None):
        return
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_size = 150
    # Settings for the overlay of rectangles
    rectangle_thickness = 2
    green = (0,255,0)
    blue = (0,0,255)
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

    return MatProcedure(frame, env)

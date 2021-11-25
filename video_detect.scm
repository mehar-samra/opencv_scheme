;;; Robotics Detection
;;;

;;; Open Web cam
(define webcam (cv2.videocapture 0))

;;; Open Robotics video
(define video (cv2.videocapture "/Users/mehar/Documents/course_footage/GOPR1142.MP4"))

(video 'set 'cv2.CAP_PROP_POS_FRAMES 600)

;;; Show n images by recursion
(define (show device n)
    (cond
      ( (>= n 1)
        (begin
          ;;; Capture an image from web camera
          (define img (device 'read))
          (define hsv (cv2.cvtcolor img 'cv2.COLOR_BGR2HSV))
          (define threshold (cv2.inrange hsv 0.5 0.0 0.0 13.5 255 255))
          (define img (draw_contours threshold img))
          ;;; Display the image
          (cv2.imshow "Scheme CV2 Demo" img)
          ;;; Recursive call
          (show device (- n 1))
        )
      )
    )
)

;;; uncomment if you want to show video
(show video 1000)

;;; show web camera
;;; (show webcam 100)

(exit)

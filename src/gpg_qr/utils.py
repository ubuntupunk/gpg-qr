# This file is currently empty, but you can move utility functions here if desired

import cv2
def display_qr_in_terminal():
        try:
           qr_img = cv2.imread("qr.png")
# initialize the cv2 QRCode detector
           detector = cv2.QRCodeDetector()
# detect and decode
           data, bbox, straight_qrcode = detector.detectAndDecode(qr_img)
# if there is a QR code
           if bbox is not None:
              print(f"QRCode data:\n{data}")
    # display the image with lines
    # length of bounding box
              n_lines = len(bbox)
           for i in range(n_lines):
        # draw all lines
              point1 = tuple(bbox[i][0])
              point2 = tuple(bbox[(i+1) % n_lines][0])
              cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

# display the result
              cv2.imshow("qr_img", qr_img)
              cv2.waitKey(0)
              cv2.destroyAllWindows()
              return true
        except Exception as e:
              print(f"An unexpected error occurred during terminal display:           {e}")
              return False



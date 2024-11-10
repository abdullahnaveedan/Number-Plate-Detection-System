import numpy as np
import cv2
import imutils
import pytesseract
import pandas as pd
import time
import os

def cvocr(cr):
    try:
        # Load and resize the image
        img = cv2.imread(cr, cv2.IMREAD_UNCHANGED)
        img = imutils.resize(img, width=500)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filter to remove noise while keeping edges sharp
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        # Detect edges
        edged = cv2.Canny(gray, 170, 200)

        # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        
        # Variable to store the number plate contour
        NumberPlateCnt = None

        # Loop through contours to find a 4-point contour (approximation of a rectangle)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:  # Look for quadrilateral shapes
                NumberPlateCnt = approx
                break

        # Check if a number plate contour was found
        if NumberPlateCnt is None:
            print("No number plate contour detected.")
            return

        # Mask out everything except the detected number plate
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        # Configuration for Tesseract OCR
        config = ('-l eng --oem 1 --psm 3')
        # config = ('-l eng+urd --oem 1 --psm 6')
        # Configuration for Tesseract OCR, focusing on English and single-line format
        # config = ('-l eng --oem 1 --psm 7')

        # Run Tesseract OCR on the masked image
        text = pytesseract.image_to_string(new_image, config=config).strip()

        # Print recognized text and handle empty results
        if text:
            print("Detected Text:", text)
        else:
            print("No text detected.")

        # Store recognized text with timestamp in CSV file
        raw_data = {'date': [time.asctime(time.localtime(time.time()))], 'v_number': [text]}
        df = pd.DataFrame(raw_data, columns=['date', 'v_number'])
        df.to_csv('data.csv', mode='a', index=False, header=not os.path.exists('data.csv'))

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    while True:
        cr = "input/" + input("Enter file name (i.e. images.jpg) : ")
        if cr == "input/Q" or cr == "input/q":
            break
        if not os.path.exists(cr):
            print(f"File does not exist at location: {cr}")
        else:
            print(f"File exists. {cr}")
            cvocr(cr)

# Vehicle Number Plate Detection System

## Overview

This system is designed to detect and recognize vehicle number plates from images. It utilizes computer vision techniques and OCR (Optical Character Recognition) to extract the alphanumeric characters from the detected number plates.

## Installation

Make sure you have Python installed. Then, install the following libraries:

```bash
pip install numpy
pip install opencv-python
pip install imutils
pip install pytesseract
pip install pandas
```

## Usage
1- Ensure you have all the required libraries installed.
2- Run the main program.
3- Provide an image containing a vehicle.
4- The program will process the image, detect the number plate, and extract the plate's characters.
5- The data will be updated in the data.csv file.

## Files
VNPDS.py: The main program for number plate detection.
data.csv: CSV file for storing detected number plates and their details.
sample_image.jpg: Example image for testing in input file

## How to Run
```bash
python main.py
```

## Example
Input Image: sample_image.jpg

## Output:
Copy code
Detected Number Plate: ABC1234
Details Updated in data.csv

## Note
Ensure that the input image is clear and well-lit for better detection results.

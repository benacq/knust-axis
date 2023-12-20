import easyocr
import cv2
import numpy as np
#from matplotlib import pyplot as plt


def extract_data(image_path):
    '''
    takes file path -> returns extracted data
    '''
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(image_path)

    surname = result[4][1]
    f_name = result[5][1]
    try:
        student_number = result[7][1].split()[2]
    except IndexError:
        student_number = result[8][1].split()[0]
    return surname, f_name, student_number

import cv2
import numpy as np

from util import BoardExtractionError

import board_extractor
import board_classifier

#import matplotlib.pyplot as plt

SIZE = (256, 256)

def classify_raw(path, board_model, sq_model):

    filename = path.split("/")[-1]
    print("Processing image {}".format(filename))

    ###############################   STEP 1    #########################################

    ## Resize image
    img = cv2.imread(path)
    comp_image = cv2.resize(img, SIZE, interpolation=cv2.INTER_AREA)
    
    ## Extract board using CNN model and contour approximation
    try: 
        board_img = board_extractor.extract_board(comp_image, img, board_model)
    except BoardExtractionError as e:
        raise e

    #del board_model
    ###############################   STEP 2    #########################################
    
    
    
    FEN, predictions, squares = board_classifier.classify_board(board_img, sq_model)
    #del sq_model
    print("Processing image {}.. DONE".format(filename))
    
    return board_img, predictions, FEN, squares

if __name__ == "__main__":

    infile = "../data/raw/IMG_4386.JPG"
    #board_img, _, FEN, squares = classify_raw(infile)

    #print(FEN)
    


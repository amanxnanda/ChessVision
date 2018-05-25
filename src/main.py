#!/anaconda/envs/tensorflow/bin/python

import sys
import cv2
from keras.models import load_model
from extract_squares import extract_squares
import numpy as np
import chess
from extract import extractBoards
from rotate_boards import rotate_board

def write_fen(fen_string, fname):
    fname = fname[:-4]
    print("Writing {}".format(fname + "_fen.txt"))
    with open(fname + "_fen.txt", "w") as f:
        f.write(fen_string)

print("Initiating main function")

filename = sys.argv[1]    #something like './uploads/img.jpg'
img = cv2.imread("../webroot/" + filename)

boards = extractBoards(img, 512, 512)
board_img = boards[0]
board_img = rotate_board(board_img)

#cv2.imwrite("test.jpg", board_img)
model = load_model('../src/square_classifier_v2.h5')

squares, names = extract_squares(board_img)
squares = np.array(squares)
squares = squares.reshape(squares.shape[0], 64, 64, 1)
squares = squares.astype('float32')
squares /= 255

predictions = model.predict(squares)
predictions = np.argmax(predictions, axis=1)

#label_names = ["R", "r", "K", "k", "Q", "q", "N", "n", "P", "p", "B", "b", "f"]
label_names  = ['B', 'K', 'N', 'P', 'Q', 'R', 'b', 'k', 'n', 'p', 'q', 'r', 'f']

board = chess.BaseBoard(board_fen=None)
    

for pred, sq in zip(predictions, names):
    if label_names[pred] == "f":
        piece = None
    else:
        piece = chess.Piece.from_symbol(label_names[pred])
        
    square = chess.SQUARE_NAMES.index(sq)
    board.set_piece_at(square, piece, promoted=False)
        
FEN = board.board_fen(promoted=False)
write_fen(FEN, "../webroot/" + filename)
# Chess Vision - a computer vision chess project

This repository contains code and resources for extracting chess positions from images using computer vision.

18/6/2018: WORK IN PROGRESS!

## Example

From *any* square input image (png, jpg, etc.), such as this one:

<img src="./img/example_raw.JPG" width="400" />

the ChessVision algorithm recognizes, extracts, and classifies any chessboard contained in the image.

Two generations of the ChessVision algorithm give the following two outputs to the example above

<p float="left">
    <img src="./img/example1.png" width="320"/>
    <img src="./img/example2.png" width="320"/>
</p>

## Earlier work

Several solutions to the chess-extraction-and-classification problem have been posed. Most rely on a combination of computer vision and machine learning, however, many different approaches are possible.

The following two links point to internet discussions about the problem at hand

+ https://www.chess.com/forum/view/endgames/convert-pngimage-file-to-pgn-or-fen
+ https://www.reddit.com/r/chess/comments/856pjh/is_there_a_way_to_get_a_fen_from_an_image_of_the/

The next links point to existing implementations

+ [chessputzer](https://github.com/metterklume/chessputzer) [(try)](https://www.ocf.berkeley.edu/~abhishek/putz/run.fcgi/upload)
+ [ChessFigRdrLite](http://www.kgrothapps.com/)
+ [chessgrabber](http://www.chessgrabber.nicolaas.net/)
+ [tensorflow_chessbot](https://github.com/Elucidation/tensorflow_chessbot)
+ [chessify](https://chessify.me/)

## ChessVision

The goal of ChessVision is to be able to correctly classify as many as possible different, valid inputs. Already the performance of the algorithm is not very bad. Since ChessVision is based on machine learning, in particular deep learning, the hope is that the performance of ChessVision will improve as more training data comes in.

We impose as few constraints on the inputs as possible, in principle any photograph of a 2D representation of a chess board should be identifyable by the algorithm. In particular, different formats such as books, screenshots, photos of screens, etc. should be allowable, under any lighting and small scale and rotational deviations. However, the input image must be square, at least 512 pixels wide, and contain exactly one chessboard filling at least 35% of the image area.

## Algorithm details

### Board extraction

The first step is to extact square chessboards from raw photographs, the following plot shows the algorithms performance on a batch of test data. 

<img src="./img/test_extraction.png" />

Board extraction is done in two steps, first the image is resized to 256x256 and fed into a deep convolutional neural network (the [unet](https://github.com/zhixuhao/unet) architecture) upon which a mask is produced, labelling each pixel as either chessboard, or not a chessboard. Next, a contour approximation algorithm approximates the mask using four points. The board is extracted from the raw image using these four points, appropriately scaled. The next image illustrates the trained models performance on a batch of training data. 

<img src="./img/training_extraction.png" />

### Board classification

The next step is to cut the board image into 64 little 64x64-pixel squares, with accompanying square-names (in order account for board orientation). We classify squares using a small convolutional network.

The performance of the current generation of square classifiers is promising; the next image shows the results on a batch of training data (99.6% accuracy)

<img src="./img/training_classification1.png" />

However, on unseen test data the algorithm fares worse, as the following figure shows

<img src="./img/test_classification.png" />

## Data, plans

Data, plans...

## Todo:

- Position Logic Checks
  - no more than two knights, bishops, rooks, kings
  - not pawn on first rank

- Recognize board rotation state! 
- Crop/resize user upload image
- UI - status/progress, hidden fields,  

- fix 2-model bug (theano kinda fixes)
  - https://github.com/keras-team/keras/issues/2397

- come up with best deployment model

## Some references

+ https://github.com/ChessCV/chess
+ http://cvgl.stanford.edu/teaching/cs231a_winter1415/prev/projects/chess.pdf
+ http://www.raspberryturk.com/details/vision.html
+ http://vision.soic.indiana.edu/b657/sp2016/projects/rkanchib/paper.pdf
+ http://indigenousengineering.com/index.php/16-ie-project/10-extract-chess-position-from-an-image-using-image-processing-algorithms
+ https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/21.pdf
+ https://ieeexplore.ieee.org/document/489004/
+ https://arxiv.org/pdf/1708.03898.pdf
+ https://ieeexplore.ieee.org/document/5967178/
+ https://web.stanford.edu/class/ee368/Project_Spring_1415/Reports/Danner_Kafafy.pdf
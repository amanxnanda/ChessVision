from __future__ import print_function

import os
import flask
import json
import base64
import numpy as np
from util import BoardExtractionError
from cv2 import imdecode, IMREAD_COLOR
from model.u_net import get_unet_256
from model.square_classifier import build_square_classifier
from chessvision import classify_raw
import tensorflow as tf
import chess
import cv2
from keras.models import load_model

#prefix = "../" # local
prefix = ""     # container
model_path = 'weights/'
model_path = os.path.join(prefix, model_path)

print("Loading models...")
board_extractor = get_unet_256()
board_extractor.load_weights(os.path.join(model_path, 'best_extractor.hdf5'))

square_classifier = load_model(os.path.join(model_path, 'best_classifier.hdf5'))
print("Loading models... DONE!")

graph = tf.get_default_graph()

def read_image_from_b64(b64string):
    buffer = base64.b64decode(b64string)
    nparr = np.frombuffer(buffer, dtype=np.uint8)
    img = imdecode(nparr, IMREAD_COLOR)
    return img

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """
    Determine if the container is working and healthy.
    In this sample container, we declare it healthy if we can load the model
    successfully.
    """
    print("Pinged")
    health = True
    status = 200 if health else 404
    return flask.Response(
        response="Yeah, bro!",
        status=status,
        mimetype='application/json')

@app.route('/invocations', methods=['POST', "GET"])
def chessvision_algo():
    """
    """
    print("Invoked")
    img = None
    flipped = None

    if flask.request.content_type == 'application/json':
        print("Got data")
        data = json.loads(flask.request.data.decode('utf-8'))
        flipped = data["flip"] == "true"
        img = read_image_from_b64(data["image"])

    else:
        print("Did not got data")
        return flask.Response(
            response="Could not parse input!",
            status=415,
            mimetype="application/json")

    # Predict

    try:
        global graph
        with graph.as_default():
            _, _, _, _, FEN, _, _ = classify_raw(img, "filename", board_extractor, square_classifier, flip=flipped)
    
    except BoardExtractionError:
        return flask.Response(
            response="ChessVision algorithm failed",
            status=500,
            mimetype="application/json")

    result = {"FEN": FEN}

    return flask.Response(response=json.dumps(result), status=200, mimetype="application/json")

if __name__ == "__main__":
    print("Running server")
    app.run(host='0.0.0.0', port=8080)

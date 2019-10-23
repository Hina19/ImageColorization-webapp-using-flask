# main.py


from . import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# import the necessary packages
from flask import Flask, request, render_template,jsonify,flash,redirect,url_for,make_response
import numpy as np

from werkzeug.utils import secure_filename

import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import tensorflow as tf
graph = tf.get_default_graph()
import numpy as np
import argparse
import cv2
import os
import glob

UPLOAD_FOLDER = 'D:/login_page/test'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "asdfghjkl!"

files = glob.glob('D:/login_page/test/*')
for f in files:
    os.remove(f)

image_path = 'D:/login_page/test/1.png'
protxt_path = 'D:/login_page/model/colorization_deploy_v2.prototxt'
model_path = 'D:/login_page/model/colorization_release_v2.caffemodel'
points_path = 'D:/login_page/model/pts_in_hull.npy'


net = cv2.dnn.readNetFromCaffe(protxt_path, model_path)
pts = np.load(points_path)

# add the cluster centers as 1x1 convolutions to the model
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

main = Blueprint('main', __name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/profile', methods=['POST'])
def upload_file():

	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			# filename = secure_filename(file.filename)
			filename='1.png'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('<=====File successfully uploaded=====>')

			return redirect('/profile')
		else:
			flash('Allowed file types are png, jpg, jpeg')
			return redirect(request.url)

@main.route('/Fill')
def colorization():
	# load the input image from disk, scale the pixel intensities to the
	# range [0, 1], and then convert the image from the BGR to Lab color
	# space
	image = cv2.imread(image_path)
	if image is None:
		flash('<=====Please upload an Image!=====>')
		return redirect('/profile')

	else:
		scaled = image.astype("float32") / 255.0
		lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

		# resize the Lab image to 224x224 (the dimensions the colorization
		# network accepts), split channels, extract the 'L' channel, and then
		# perform mean centering
		resized = cv2.resize(lab, (224, 224))
		L = cv2.split(resized)[0]
		L -= 50

		# pass the L channel through the network which will *predict* the 'a'
		# and 'b' channel values
		'print("[INFO] colorizing image...")'
		net.setInput(cv2.dnn.blobFromImage(L))
		ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

		# resize the predicted 'ab' volume to the same dimensions as our
		# input image
		ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

		# grab the 'L' channel from the *original* input image (not the
		# resized one) and concatenate the original 'L' channel with the
		# predicted 'ab' channels
		L = cv2.split(lab)[0]
		colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

		# convert the output image from the Lab color space to RGB, then
		# clip any values that fall outside the range [0, 1]
		colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
		colorized = np.clip(colorized, 0, 1)

		# the current colorized image is represented as a floating point
		# data type in the range [0, 1] -- let's convert to an unsigned
		# 8-bit integer representation in the range [0, 255]
		colorized = (255 * colorized).astype("uint8")
		ret, png = cv2.imencode('.png', colorized)
		response = make_response(png.tobytes())
		response.headers['Content-Type'] = 'image/png'
		files = glob.glob('D:/login_page/test/*')
		for f in files:
			os.remove(f)
		return response


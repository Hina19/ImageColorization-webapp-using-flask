# ImageColorization-webapp-using-flask
<h3>Team: Standalone</h3><br>
Objective:
  <p>Simple application for coloring the balck and white images using pretrained <a href="https://drive.google.com/file/d/1GYBNq9USP1c_waUiiz6Lr0PJLH_ebmRv/view?usp=sharing">caffe model</a> (download and save that model in folder model).</p><br>
For Authentication:
<ul>
  <li>Use the Flask-Login library for session management</li>
<li>Use the built-in Flask utility for hashing passwords</li>
<li>Add protected pages to our app for logged in users only</li>
<li>Use Flask-SQLAlchemy to create a user model</li>
<li>Create sign up and login forms for our users to create accounts and login</li>
<li>Flash error messages back to users when something goes wrong</li>
  <li>Use information from the user's account to display on the profile page</li></ul>
<br>
For Model:
  <p>
 The technique that we’ll be using here today is from Zhang et al.’s 2016 ECCV paper, <a href="http://richzhang.github.io/colorization/">Colorful Image Colorization</a>.

Previous approaches to black and white image colorization relied on manual human annotation and often produced desaturated results that were not “believable” as true colorizations.

Zhang et al. decided to attack the problem of image colorization by using Convolutional Neural Networks to “hallucinate” what an input grayscale image would look like when colorized.

To train the network Zhang et al. started with the <a href="http://image-net.org/">ImageNet dataset</a> and converted all images from the RGB color space to the Lab color space.

Similar to the RGB color space, the Lab color space has three channels. But unlike the RGB color space, Lab encodes color information differently:
<ul>
  <li>The L channel encodes lightness intensity only</li>
  <li>The a channel encodes green-red.</li>
  <li>And the b channel encodes blue-yellow</li></ul></p>

Running the application:
<pre> export FLASK_APP=ImageColorization
      export FLASK_DEBUG=1
      flask run
Application run in local environment by running  with address 127.0.0.1:5000</pre>


<h4>Screenshots:</h4>

1.HOME PAGE:

<img src="https://i.imgur.com/bSfXzbv.png" >

2.SIGN_UP PAGE:

<img src="https://i.imgur.com/75cRqym.png">

3.LOGIN PAGE:

<img src="https://i.imgur.com/TXCGaLi.png">

4.PROFILE PAGE:

<img src="https://i.imgur.com/9RWLlPG.png">

5. UPLOAD IMAGE:

<img src="https://i.imgur.com/9RWLlPG.png">

6. RESULTS:

<img src="https://i.imgur.com/LFaVA4T.png">
<img src="https://i.imgur.com/MT3zmz9.png">
<img src="https://i.imgur.com/sgiu17j.png">

<h4>References:</h4>

<a href="https://flask.palletsprojects.com/en/1.1.x/quickstart/">https://flask.palletsprojects.com/en/1.1.x/quickstart/</a>
<a href="https://scotch.io/tutorials/authentication-and-authorization-with-flask-login">https://scotch.io/tutorials/authentication-and-authorization-with-flask-login</a>
<a href="https://www.pyimagesearch.com/2019/02/25/black-and-white-image-colorization-with-opencv-and-deep-learning/">https://www.pyimagesearch.com/2019/02/25/black-and-white-image-colorization-with-opencv-and-deep-learning/</a>

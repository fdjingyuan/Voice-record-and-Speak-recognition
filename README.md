## Voice Recogition

<<<<<<< HEAD

This project is a voice recogition based on PyTorch, Flask and Vue.js. We trained ResNet and VGG networks in PyTorch for word classifcation and achieved over 99% accuracy. To show the result, we designed a web application which can record, play and recognize audio using Vue.js and Flask.

![](https://gitee.com/hzy46/voice-recognition/raw/master/images/show.png)
=======
> A Vue.js project for word voice recognition

Since this project has been build, you just need to install python dependencies and run the server if you want to use the application.
## Python dependencies

``` bash
pip install -r requirements.txt
```
## server
``` bash
python -m pysrc.server
```

If you modify the code and want to re-run it, try as following:
>>>>>>> e15f56317cf0e246c16514141bcaec0eba49164f


### Requirements

Python3, PyTorch >= 0.4.0, Flask and Vue.js.

Please install all the Python dependencies using:

```
pip install -r requirements.txt
```

### Quick Start

First, run the front-end server:

```
# install dependencies
npm install

<<<<<<< HEAD
# build
npm run build

# serve with hot reload at localhost:8080
npm run dev
```

Then run the api server:
```
python -m pysrc.server
```

Please visit localhost:8080 to test the application.
=======
# build for production with minification
npm run build

# serve with hot reload at localhost:8080
npm run dev

>>>>>>> e15f56317cf0e246c16514141bcaec0eba49164f


### Train a Model

If you want to train your own model, please refer to the following steps.

#### Preprocess

<<<<<<< HEAD
```
# generate data
=======
## train model
``` bash
# pre-process
## deal with data
>>>>>>> e15f56317cf0e246c16514141bcaec0eba49164f
python -m script.gen_data 

# split data to train.txt and test.txt
python -m script.train_test_split 

# calculate MFCC MEL feature
python -m script.cal_mean_std.py 
```

#### Start Training

```
python -m pysrc.train
```

Models will be saved to a folder named "models/".


<<<<<<< HEAD

=======
>>>>>>> e15f56317cf0e246c16514141bcaec0eba49164f

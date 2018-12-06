## Voice Recogition


This project is a voice recogition based on PyTorch, Flask and Vue.js. We trained ResNet and VGG networks in PyTorch for word classifcation and achieved over 99% accuracy. To show the result, we designed a web application which can record, play and recognize audio using Vue.js and Flask.

![](https://gitee.com/hzy46/voice-recognition/raw/master/images/show.png)


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


### Train a Model

If you want to train your own model, please refer to the following steps.

#### Preprocess

```
# generate data
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




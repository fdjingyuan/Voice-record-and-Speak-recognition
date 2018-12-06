# Voice Recogition


This project is a voice recogition based on PyTorch, Flask and Vue.js. This project trained ResNet and VGG networks in PyTorch for word classifcation and achieved over 99% accuracy. 

There is also a friendly front-enf for web application which can record, play and recognize audio using Vue.js and Flask.

![](https://github.com/fdjingyuan/Voice-record-and-Speak-recognition/blob/master/img/recognize.jpg)

## Directly running the application
Since this project has been build, you just need to install python dependencies and run the server if you want to use the application.
### Python dependencies
``` bash
pip install -r requirements.txt
```
### Run the server
``` bash
python -m pysrc.server
```
Enter http://127.0.0.1:5000/ to access the web application.


## Modify for your own project
If you modify the code and want to re-run it, try as following:

### Run front-end
First you need to download and install node. js, then

```
# install dependencies
npm install

# build for production with minification
npm run build

# serve with hot reload at localhost:8080
npm run dev
```

Then run the back-end server:
```
python -m pysrc.server
```




### Train a Model

If you want to train your own model, please refer to the following steps.

#### Preprocess

```
# pre-process
## deal with data
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

#### Algorithm framework

![](https://github.com/fdjingyuan/Voice-record-and-Speak-recognition/blob/master/img/model.png)

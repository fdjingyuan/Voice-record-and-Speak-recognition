# voice_pj

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

## Build Setup

``` bash
# install dependencies
npm install

# build for production with minification
npm run build

# serve with hot reload at localhost:8080
npm run dev


# run e2e tests
npm run e2e

# run all tests
npm test
```


## train model
``` bash
# pre-process
## deal with data
python -m script.gen_data 
## generate train.txt test.txt
python -m script.train_test_split 
## calculate MFCC MEL feature
python -m script.cal_mean_std.py 

#train
python -m pysrc.train



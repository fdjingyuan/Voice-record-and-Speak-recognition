# voice_pj

#


> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run e2e tests
npm run e2e

# run all tests
npm test
```


#train model
# pre-process
## deal with data
python -m script.gen_data 
## generate train.txt test.txt
python -m script.train_test_split 
## calculate MFCC MEL feature
python -m script.cal_mean_std.py 

#train
python -m pysrc.train


#server
python -m pysrc.server


import json
from flask import Flask
from flask import render_template, jsonify, request, make_response
import base64
from pysrc.interface import WavRecgnition
from functools import wraps
import io
import librosa
from pysrc import const
import uuid
import shutil

app = Flask(__name__)
interface = WavRecgnition(use_device='cpu')
file = None

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


@app.route('/')
def hello():
    return make_response("Hello World!")


@app.route('/api', methods=['OPTIONS'])
def cross_domain():
    data = request.get_data().strip()
    print(data)
    response = make_response(json.dumps({}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Origin, X-Requested-With, Content-Type, Accept"
    response.headers['Access-Control-Allow-Headers'] = allow_headers
    return response


@app.route('/api', methods=['GET', 'POST'])
def rec():
    base64_data = request.get_data().strip()
    base64_data = base64_data[base64_data.find(b',') + 1:]
    filename = 'tmp/' + str(uuid.uuid1()) + '.wav'
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(base64_data))
    samples, _ = librosa.load(filename, sr=const.SR)
    print('audio', len(samples) / const.SR, 'second')
    result, result_prob = interface.classify(samples)
    response = make_response(json.dumps({'result': result, 'prob': result_prob}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(debug=False)

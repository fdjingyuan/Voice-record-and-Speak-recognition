import json
import os
from flask import Flask
from flask import render_template, jsonify, request, make_response, send_from_directory
import base64
from pysrc.interface import WavRecgnition
from functools import wraps
import librosa
from pysrc import const
import uuid
import shutil

#Notice: flask & vue, use "dist/index.html", should bind the directory
app = Flask(__name__,
            static_folder = '../dist/static',
            template_folder='../dist')

interface = WavRecgnition(use_device='cpu')
file = None

# @app.route('/api', methods=['OPTIONS'])
# def cross_domain():
#     data = request.get_data().strip()
#     print(data)
#     response = make_response(json.dumps({}))
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#     allow_headers = "Origin, X-Requested-With, Content-Type, Accept"
#     response.headers['Access-Control-Allow-Headers'] = allow_headers
#     return response


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

#Notice: binding directory
@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    path = path.strip()
    #worker.js should return to the path of js not "index.html"
    if path.endswith('js'):
        return render_template(path)
    return render_template("index.html")


if __name__ == '__main__':
    print("run..")
    app.run(debug=False)

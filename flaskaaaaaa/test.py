from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app, resources={r"/apitest": {"origins": "*"}})
cors = CORS(app, resources={r"/apitest": {"origins": "http://localhost:port"}})

@app.route('/')
def hello_world():
    return 'Hello World!' 


@app.route('/apitest/<float:lon>/<float:latt>')
@cross_origin(origin='*',headers=['Content- Type','Authorization']) 
def apitest(lon,latt):
    text = {'value':'123'}
#    return 'coords: ' + str(lon) +':'+ str(latt)
    return jsonify(text)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


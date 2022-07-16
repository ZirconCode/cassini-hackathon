from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from lyg import WebsiteGetter, HEATMAP
import numpy as np

app = Flask(__name__)

app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/apitest": {"origins": "http://localhost:port"}})


@app.route("/api/v1/<float:lat>/<float:lon>")
@cross_origin(origin="*", headers=["Content- Type", "Authorization"])
def apitest(lat, lon):
    w = WebsiteGetter(HEATMAP)
    text = {"value": str(int(np.round(w.get(lat, lon))))}
    return jsonify(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0")

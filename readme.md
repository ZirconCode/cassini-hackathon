# Live your Green

This is the Live your Green submission for the first Cassini Hackathon (Switzerland Hub). The repository runs on the provided CREODIAS VM. The project prototype consists of a few components.

## Satellite Data

We transform Sentinel 2 data into QGIS (see satellite folder), and apply the NDVI and NDWI to the zurich region. For the prototype we've picked one cloudless day only. We export this as a .tif for further processing in python (see processing folder). 

## Server/API

Our frontend consists of dynamic (mobile and desktop adapting) Vue.js on an npm server. This calls our API which provides the backend, ingesting our processed python code.

## Getting started

```sh
pip install -e LiveYourGreens

export FLASK_APP=server.py

flask run --host=0.0.0.0
```

Try for example: `http://localhost:5000/api/v1/47.35/8.5`.

#!/usr/bin/env python3
from config.config import AppConfig
from swagger_server import app, encoder
from flask_cors import CORS

app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml')

app.app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app.app, resources={r"/v1/*": {"origins": "*"}})


@app.route('/')
def index():
    return "SmartCanteen API Version {0}".format(AppConfig.VERSION)


def main():
    app.run(port=5000)


if __name__ == '__main__':
    main()


@app.app.after_request
def after_request(response):
  print("after_request")
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

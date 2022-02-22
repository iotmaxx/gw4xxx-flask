from flask import Flask
from flask_restful import Api, Resource

apiVersion = "0.1.1"
theApplication = Flask(__name__)
#theApplication.config['SERVER_NAME'] = '192.168.1.1:5000'
theApi = Api(theApplication)

from gw4xxx_flask.gw4xxx.deviceInfo import DeviceInfoAPI

theApi.add_resource(DeviceInfoAPI, '/', endpoint='gw4xxx_deviceInfo')

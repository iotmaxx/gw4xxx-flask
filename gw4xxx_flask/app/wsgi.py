#from flask import Flask
#from flask_restful import Api, Resource
from gw4xxx_flask.app import theApi, apiVersion, theApplication

from gw4xxx_flask.gw4xxx.deviceInfo import DeviceInfoAPI

theApi.add_resource(DeviceInfoAPI, '/', endpoint='gw4xxx_deviceInfo')

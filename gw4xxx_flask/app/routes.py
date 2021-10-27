from app import theApplication
from flask_restful import Api, Resource
from gw4xxx.deviceInfo import DeviceInfoAPI

theApi = Api(theApplication)


class TestAPI(Resource):
    def get(self):
        return { 'hello' : 'world' }

theApi.add_resource(DeviceInfoAPI, '/', endpoint='gw4xxx_deviceInfo')

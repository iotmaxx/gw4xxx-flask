from flask_restful import Resource, fields, marshal

class GW4x01API(Resource):
    def get(self):
         return { 'api' : 'GW4x01API' }

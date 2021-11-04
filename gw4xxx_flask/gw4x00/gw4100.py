from flask_restful import Resource, fields, marshal
from app import theApi, theApplication
from gw4x00.gw4x00_io import GW4x00GPI, GW4x00GPIO

theApi.add_resource(GW4x00GPI, '/gw4100/gpi', endpoint='gw4100_gpi')
theApi.add_resource(GW4x00GPIO, '/gw4100/gpio/<int:id>', endpoint='gw4100_gpio')

gw4100gpi_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4100_gpi', absolute=True)
}

gw4100gpio_fields = {
    "id": fields.Integer,
    "uri": fields.String
}

gw4100gpios_fields = {
    "num": fields.Integer,
    "gpios": fields.List(fields.Nested(gw4100gpio_fields))
}

gw4100_fields = {
    "GPI": fields.Nested(gw4100gpi_fields),
    "GPIO": fields.Nested(gw4100gpios_fields),
    "uri":  fields.Url('gw4100', absolute=True)
}

with theApplication.test_request_context():
    theGW4100 = {
        "GPI":  { "num": 4 },
        "GPIO": { "num": 2, "gpios": [ { "id": 0, "uri":  theApi.url_for(GW4x00GPIO, id=0, _external=True) }, { "id": 1, "uri":  theApi.url_for(GW4x00GPIO, id=1, _external=True) } ] }
    }

#print(theGW4100)

class GW4100API(Resource):
    def get(self):
        return marshal(theGW4100, gw4100_fields), 200


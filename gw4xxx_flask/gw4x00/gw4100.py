""" 
gw4xxx-hal - IoTmaxx Gateway Hardware Abstraction Layer
Copyright (C) 2021 IoTmaxx GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from flask_restful import Resource, fields, marshal
from gw4xxx_flask.app import theApi, theApplication
from gw4xxx_flask.gw4x00.gw4x00_io import GW4x00GPI, GW4x00GPIO
from gw4xxx_flask.gw4x00.gw4x00_w1 import GW4x00W1, GW4x00W1DEV
from gw4xxx_flask.gw4x00.gw4x00_rs485 import GW4x00RS485
#from gw4x00.gw4x00_eeprom2 import GW4x00GPI2, GW4x00GPIO2

theApi.add_resource(GW4x00GPI, '/gw4100/gpi', endpoint='gw4100_gpi')
theApi.add_resource(GW4x00GPIO, '/gw4100/gpio/<int:id>', endpoint='gw4100_gpio')
theApi.add_resource(GW4x00W1, '/gw4100/w1', endpoint='gw4100_w1')
theApi.add_resource(GW4x00W1DEV, '/gw4100/w1/<int:id>', endpoint='gw4100_w1device')

theApi.add_resource(GW4x00RS485, '/gw4100/rs485', endpoint='gw4100_rs485')

gw4100gpi_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4100_gpi', absolute=True)
}

gw4100gpio_fields = {
    "id": fields.Integer,
    "uri": fields.Url('gw4100_gpio', absolute=True)
}

gw4100gpios_fields = {
    "num": fields.Integer,
    "gpios": fields.List(fields.Nested(gw4100gpio_fields))
}

gw4100w1_fields = {
    "uri":  fields.Url('gw4100_w1', absolute=True)
}

gw4100_fields = {
    "GPI": fields.Nested(gw4100gpi_fields),
    "GPIO": fields.Nested(gw4100gpios_fields),
    "w1": fields.Nested(gw4100w1_fields),
    "uri":  fields.Url('gw4100', absolute=True)
}

with theApplication.test_request_context():
    theGW4100 = {
        "GPI":  { "num": 4 },
        "GPIO": { "num": 2, "gpios": [ { "id": 0 }, { "id": 1 } ] },
        "w1": {}
    }

#print(theGW4100)

class GW4100API(Resource):
    def get(self):
        return marshal(theGW4100, gw4100_fields), 200


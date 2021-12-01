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
from app import theApi, theApplication
from gw4x00.gw4x00_io import GW4x00GPI, GW4x00GPIO
#from gw4x00.gw4x00_eeprom2 import GW4x00GPI2, GW4x00GPIO2
from gw4x00.gw4x00_eeprom import MainBoardEEPROM

theApi.add_resource(MainBoardEEPROM, '/gw4x00/eeprom', endpoint='gw4x00_eeprom')

theApi.add_resource(GW4x00GPI, '/gw4100/gpi', endpoint='gw4100_gpi')
theApi.add_resource(GW4x00GPIO, '/gw4100/gpio/<int:id>', endpoint='gw4100_gpio')

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

gw4100_fields = {
    "GPI": fields.Nested(gw4100gpi_fields),
    "GPIO": fields.Nested(gw4100gpios_fields),
    "uri":  fields.Url('gw4100', absolute=True)
}

with theApplication.test_request_context():
    theGW4100 = {
        "GPI":  { "num": 4 },
        "GPIO": { "num": 2, "gpios": [ { "id": 0 }, { "id": 1 } ] }
    }

#print(theGW4100)

class GW4100API(Resource):
    def get(self):
        return marshal(theGW4100, gw4100_fields), 200


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
from gw4xxx_flask.gw4x04.gw4x04_io import GW4x04GPI, GW4x04IsoIn, GW4x04IsoOut
from gw4xxx_flask.gw4x04.gw4x04_adc import GW4x04RTD, GW4x04CurrentLoopIn, GW4x04CurrentLoopOut

theApi.add_resource(GW4x04GPI, '/gw4x04/gpi', endpoint='gw4x04_gpi')
theApi.add_resource(GW4x04IsoIn, '/gw4x04/isoin', endpoint='gw4x04_isoin')
theApi.add_resource(GW4x04IsoOut, '/gw4x04/isoout/<int:id>', endpoint='gw4x04_isoout')
theApi.add_resource(GW4x04RTD, '/gw4x04/rtd', endpoint='gw4x04_rtd')
theApi.add_resource(GW4x04CurrentLoopIn, '/gw4x04/currentloopin', endpoint='gw4x04_currentloopin')
theApi.add_resource(GW4x04CurrentLoopOut, '/gw4x04/currentloopout', endpoint='gw4x04_currentloopout')

gw4x04gpi_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x04_gpi', absolute=True)
}

gw4x04isoin_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x04_isoin', absolute=True)
}

gw4x04isoout_fields = {
    "id": fields.Integer,
    "uri": fields.Url('gw4x04_isoout', absolute=True)
}

gw4x04isoouts_fields = {
    "num": fields.Integer,
    "isoouts": fields.List(fields.Nested(gw4x04isoout_fields))
}

gw4x04rtd_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x04_rtd', absolute=True)
}

gw4x04currentloopin_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x04_currentloopin', absolute=True)
}

gw4x04currentloopout_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x04_currentloopout', absolute=True)
}

gw4x04_fields = {
    "GPI":              fields.Nested(gw4x04gpi_fields),
    "IsoIn":            fields.Nested(gw4x04isoin_fields),
    "IsoOut":           fields.Nested(gw4x04isoouts_fields),
    "RTD":              fields.Nested(gw4x04rtd_fields),
    "CurrentLoopIn":    fields.Nested(gw4x04currentloopin_fields),
    "CurrentLoopOut":   fields.Nested(gw4x04currentloopout_fields),
    "uri":              fields.Url('gw4x04', absolute=True)
}

with theApplication.test_request_context():
    theGW4x04 = {
        "GPI":  { "num": 4 },
        "IsoIn":  { "num": 4 },
        "IsoOut": { "num": 2, "isoouts": [ { "id": 0 }, { "id": 1 } ] },
        "RTD":  { "num": 4 },
        "CurrentLoopIn":  { "num": 4 },
        "CurrentLoopOut":  { "num": 1 },
    }


class GW4x04API(Resource):
    def get(self):
          return marshal(theGW4x04, gw4x04_fields), 200

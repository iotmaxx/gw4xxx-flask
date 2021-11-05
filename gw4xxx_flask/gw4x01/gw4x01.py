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
from gw4x01.gw4x01_io import GW4x01GPI, GW4x01IsoIn, GW4x01IsoOut
from gw4x01.gw4x01_adc import GW4x01RTD, GW4x01CurrentLoopIn, GW4x01CurrentLoopOut

theApi.add_resource(GW4x01GPI, '/gw4x01/gpi', endpoint='gw4x01_gpi')
theApi.add_resource(GW4x01IsoIn, '/gw4x01/isoin', endpoint='gw4x01_isoin')
theApi.add_resource(GW4x01IsoOut, '/gw4x01/isoout/<int:id>', endpoint='gw4x01_isoout')
theApi.add_resource(GW4x01RTD, '/gw4x01/rtd', endpoint='gw4x01_rtd')
theApi.add_resource(GW4x01CurrentLoopIn, '/gw4x01/currentloopin', endpoint='gw4x01_currentloopin')
theApi.add_resource(GW4x01CurrentLoopOut, '/gw4x01/currentloopout', endpoint='gw4x01_currentloopout')

gw4x01gpi_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x01_gpi', absolute=True)
}

gw4x01isoin_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x01_isoin', absolute=True)
}

gw4x01isoout_fields = {
    "id": fields.Integer,
    "uri": fields.String
}

gw4x01isoouts_fields = {
    "num": fields.Integer,
    "isoouts": fields.List(fields.Nested(gw4x01isoout_fields))
}

gw4x01rtd_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x01_rtd', absolute=True)
}

gw4x01currentloopin_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x01_currentloopin', absolute=True)
}

gw4x01currentloopout_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x01_currentloopout', absolute=True)
}

gw4x01_fields = {
    "GPI":              fields.Nested(gw4x01gpi_fields),
    "IsoIn":            fields.Nested(gw4x01isoin_fields),
    "IsoOut":           fields.Nested(gw4x01isoouts_fields),
    "RTD":              fields.Nested(gw4x01rtd_fields),
    "CurrentLoopIn":    fields.Nested(gw4x01currentloopin_fields),
    "CurrentLoopOut":   fields.Nested(gw4x01currentloopout_fields),
    "uri":              fields.Url('gw4x01', absolute=True)
}

with theApplication.test_request_context():
    theGW4x01 = {
        "GPI":  { "num": 4 },
        "IsoIn":  { "num": 4 },
        "IsoOut": { "num": 2, "isoouts": [ { "id": 0, "uri":  theApi.url_for(GW4x01IsoOut, id=0, _external=True) }, { "id": 1, "uri":  theApi.url_for(GW4x01IsoOut, id=1, _external=True) } ] },
        "RTD":  { "num": 4 },
        "CurrentLoopIn":  { "num": 4 },
        "CurrentLoopOut":  { "num": 1 },
    }


class GW4x01API(Resource):
    def get(self):
          return marshal(theGW4x01, gw4x01_fields), 200

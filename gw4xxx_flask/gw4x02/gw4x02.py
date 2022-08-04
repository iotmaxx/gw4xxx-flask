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
from gw4xxx_flask.gw4x02.gw4x02_io import GW4x02IsoIn, GW4x02IsoOut

theApi.add_resource(GW4x02IsoIn, '/gw4x02/isoin', endpoint='gw4x02_isoin')
theApi.add_resource(GW4x02IsoOut, '/gw4x02/isoout/<int:id>', endpoint='gw4x02_isoout')

gw4x02isoin_fields = {
    "num": fields.Integer,
    "uri":  fields.Url('gw4x02_isoin', absolute=True)
}

gw4x02isoout_fields = {
    "id": fields.Integer,
    "uri": fields.Url('gw4x02_isoout', absolute=True)
}

gw4x02isoouts_fields = {
    "num": fields.Integer,
    "isoouts": fields.List(fields.Nested(gw4x02isoout_fields))
}


gw4x02_fields = {
    "IsoIn":            fields.Nested(gw4x02isoin_fields),
    "IsoOut":           fields.Nested(gw4x02isoouts_fields),
    "uri":              fields.Url('gw4x02', absolute=True)
}

with theApplication.test_request_context():
    theGW4x02 = {
        "IsoIn":  { "num": 16 },
        "IsoOut": { "num": 4, "isoouts": [ { "id": 0 }, { "id": 1 }, { "id": 2 }, { "id": 3 } ] },
    }


class GW4x02API(Resource):
    def get(self):
          return marshal(theGW4x02, gw4x02_fields), 200

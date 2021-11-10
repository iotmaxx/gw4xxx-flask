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
from gw4x90.gw4x90_dac import GW4x90DACChip#, GW4x90DACChannel
from gw4x90.gw4x90_currentLoop import GW4x90CurrentLoopOutChannel

theApi.add_resource(GW4x90DACChip, '/gw4x90/dac/<int:chip>', endpoint='gw4x90_dac_chip')
#theApi.add_resource(GW4x90CurrentLoopOut, '/gw4x90/currentloop', endpoint='gw4x90_currentloop')
theApi.add_resource(GW4x90CurrentLoopOutChannel, '/gw4x90/currentloopout/<int:channel>', endpoint='gw4x90_currentloopoutchannel')

gw4x90currentloopoutchannel_fields = {
    "channel":          fields.Integer,
    "uri":              fields.Url('gw4x90_currentloopoutchannel', absolute=True)
}

gw4x90currentloopout_fields = {
    "num":              fields.Integer,
    "channels":         fields.List(fields.Nested(gw4x90currentloopoutchannel_fields)),
}

gw4x90dacchips_fields = {
    "chip":             fields.Integer,
#    "num_channels":     fields.Integer,
    "uri":              fields.Url('gw4x90_dac_chip', absolute=True)
}

gw4x90dac_fields = {
    "num_chips":        fields.Integer,
    "chips":            fields.List(fields.Nested(gw4x90dacchips_fields)),
}

gw4x90_fields = {
    "DAC":              fields.Nested(gw4x90dac_fields),
    "CurrentLoopOut":   fields.Nested(gw4x90currentloopout_fields),
    "uri":              fields.Url('gw4x90', absolute=True)
}

with theApplication.test_request_context():
    theGW4x90 = {
        "DAC":  { "num_chips": 4, "chips": [] },
        "CurrentLoopOut":  { "num": 4, "channels": [] },
    }
    for chip in range(4):
        theChip = {
            "num_channels": 4,
            "chip": chip,
            "channels": []
        }
        # for channel in range(4):
        #     theChannel = {
        #         "channel": channel,
        #         "chip": chip
        #     }
        #     theChip["channels"].append(theChannel)
        theGW4x90["DAC"]["chips"].append(theChip)
    for channel in range(4):
        theChannel = {
            "channel": channel
        }        
        theGW4x90["CurrentLoopOut"]["channels"].append(theChannel)

class GW4x90API(Resource):
    def get(self):
        return marshal(theGW4x90, gw4x90_fields), 200

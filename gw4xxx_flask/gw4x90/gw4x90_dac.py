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
from flask_restful import Resource, fields, marshal, reqparse, inputs, abort
from gw4xxx_flask.app import theApi, theApplication, reqparser
from gw4xxx_hal.gw4x90 import analogIOControl
import os

gw4x90dacchannelset_fields = {
    "chip":             fields.Integer,
    "channel":          fields.Integer,
    "uri":              fields.Url('gw4x90_dac_channel', absolute=True),
}

class GW4x90DACChannel(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('voltage', type = reqparser.float_range(min=0.0, max=24.0), required = True,
            help = 'invalid voltage: {error_msg}', location = 'json')
        super(GW4x90DACChannel, self).__init__()

    def get(self, chip, channel):
        return { 'DACChannel': marshal({'chip':chip, 'channel':channel }, gw4x90dacchannelset_fields)}

    def put(self, chip, channel):
        args = self.putparse.parse_args()
        analogIOControl.setVoltage(chip, channel, float(args['voltage']))
        return { 'DACChannel': marshal({'chip':chip, 'channel':channel }, gw4x90dacchannelset_fields)}

theApi.add_resource(GW4x90DACChannel, '/gw4x90/dac/<int:chip>/<int:channel>', endpoint='gw4x90_dac_channel')

gw4x90dacchannel_fields = {
    "chip":             fields.Integer,
    "channel":          fields.Integer,
    "voltage":          fields.Float,
    "vref":             fields.Boolean,
    "gain":             fields.Boolean,
    "power_state":      fields.Integer,
    "uri":              fields.Url('gw4x90_dac_channel', absolute=True),
}

gw4x90dacchips_fields = {
   "chip":             fields.Integer,
   "num_channels":     fields.Integer,
   "channels":         fields.List(fields.Nested(gw4x90dacchannel_fields)),
}

class GW4x90DACChip(Resource):
    def get(self, chip):
        theGW4x90DACChip = { "chip": chip, "num_channels": 4, "channels": [] }
        theCurrentSettings = analogIOControl.getCurrentSettings(chip)
        for channel in range(4):
            theChannel = {
                "channel": channel,
                "chip": chip,
            }
            theChannel.update(theCurrentSettings[channel])
            theGW4x90DACChip["channels"].append(theChannel)

        return marshal(theGW4x90DACChip, gw4x90dacchips_fields), 200



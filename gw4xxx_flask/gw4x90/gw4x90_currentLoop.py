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
from gw4xxx_hal.gw4x90 import currentLoopControl
from gw4xxx_hal.gw4xxx.exceptions import ChannelPoweredDownError
from app import reqparser

gw4x90currentloopoutchannel_fields = {
    "channel":          fields.Integer,
    "available":        fields.Boolean,
    "powerdown":        fields.Boolean,
    "current":          fields.Float,
    "uri":              fields.Url('gw4x90_currentloopoutchannel', absolute=True)
}

class GW4x90CurrentLoopOutChannel(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('current', type = reqparser.float_range(min=0.0, max=25.0), required = True,
            help = 'invalid current: {error_msg}', location = 'json')
        super(GW4x90CurrentLoopOutChannel, self).__init__()

    def _createResponse(self, channel):
        try:
            theCurrent = currentLoopControl.getOutputCurrent(channel)
            powerdown = False
            available = True
        except ChannelPoweredDownError:
            theCurrent = 0
            powerdown = True
            available = True
        except OSError:
            theCurrent = 0
            powerdown = False
            available = False

        return { 'GW4x90CurrentLoopOutChannel': marshal({ 'channel':channel, 'current': theCurrent, 'available': available, 'powerdown': powerdown }, gw4x90currentloopoutchannel_fields)}

    def get(self, channel):
        return self._createResponse(channel)

    def put(self, channel):
        args = self.putparse.parse_args()
        try:
            currentLoopControl.setOutputCurrent(channel,float(args['current']))
        except (ChannelPoweredDownError,OSError):
            pass
        return self._createResponse(channel)



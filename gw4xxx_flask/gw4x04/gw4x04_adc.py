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
from flask_restful import Resource, fields, marshal, reqparse
from gw4xxx_hal.gw4x04 import adcControl
from gw4xxx_hal.gw4xxx.exceptions import ChannelPoweredDownError
from gw4xxx_flask.app import reqparser, theApplication
import os

loopOut_fields = {
    "value":        fields.Float,
    "powerDown":    fields.Boolean,
    'uri':          fields.Url('gw4x04_currentloopout', absolute=True)
}

rtd_fields = {
    "values":   fields.List(fields.Float),
    'uri':      fields.Url('gw4x04_rtd', absolute=True)
}

loopIn_fields = {
    "values":   fields.List(fields.Float),
    'uri':      fields.Url('gw4x04_currentloopin', absolute=True)
}

#if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
if (not theApplication.debug) or os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get('SERVER_SOFTWARE') is not None:
    theADC = adcControl.GW4x04ADC()

class GW4x04RTD(Resource):
    def get(self):
        numADCs=4
        values = []
        for adc in range(numADCs):
            values.append(theADC.readRTDValue(adc))
        return { 'rtds':  marshal({ "values": values }, rtd_fields) }

class GW4x04CurrentLoopIn(Resource):
    def get(self):
        numADCs=4
        values = []
        for adc in range(numADCs):
            values.append(theADC.readCurrentLoop(adc))
        return { 'currentLoopInputs':  marshal({ "values": values }, loopIn_fields) }

class GW4x04CurrentLoopOut(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('current', type = reqparser.float_range(min=0.0, max=20.0), required = True,
            help = 'invalid current: {error_msg}', location = 'json')
        super(GW4x04CurrentLoopOut, self).__init__()

    def _getChannelData(self):
        theData = {}
        try:
            theData['value'] = theADC.getOutputCurrent()
            theData['powerDown'] = False
        except ChannelPoweredDownError:
            theData['value'] = 0
            theData['powerDown'] = True
        return theData

    def get(self):
        return { 'currentLoopOutput':  marshal(self._getChannelData(), loopOut_fields) }

    def put(self):
        args = self.putparse.parse_args()
        current = float(args['current'])
        theADC.setOutputCurrent(current)
        if current == 0:
            theADC.powerDownChannel()
        return { 'currentLoopOutput':  marshal(self._getChannelData(), loopOut_fields) }

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
from gw4xxx_hal.gw4x01 import adcControl
import os

rtd_fields = {
    "values":   fields.List(fields.Float),
    'uri':      fields.Url('gw4x01_gw4x01_rtd', absolute=True)
}

loopIn_fields = {
    "values":   fields.List(fields.Float),
    'uri':      fields.Url('gw4x01_currentloopin', absolute=True)
}

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    theADC = adcControl.GW4x01ADC()

class GW4x01RTD(Resource):
    def get(self):
        numADCs=4
        values = []
        for adc in range(numADCs):
            values.append(theADC.readRTDValue(adc))
        return { 'rtds':  marshal({ "values": values }, rtd_fields) }

class GW4x01CurrentLoopIn(Resource):
    def get(self):
        numADCs=4
        values = []
        for adc in range(numADCs):
            values.append(theADC.readCurrentLoop(adc))
        return { 'currentLoopInputs':  marshal({ "values": values }, loopIn_fields) }

class GW4x01CurrentLoopOut(Resource):
    def get(self):
         return { 'api' : 'GW4x01CurrentLoopOut' }

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
from gw4xxx_hal.gw4x90 import analogIOControl

gw4x90adc_fields = {
    '1-wire':   fields.Float,
    'inputs':   fields.List(fields.Float),
    'current':  fields.Float,
    'uri':      fields.Url('gw4x90_adc', absolute=True)
}

class GW4x90ADC(Resource):
    def get(self):
        adcValues = {}
        adcValues['1-wire'] = analogIOControl.readOneWireVoltage()
        adcValues['inputs'] = [ analogIOControl.readGPIOVoltage(0), analogIOControl.readGPIOVoltage(1) ]
        adcValues['current'] = analogIOControl.readCurrentLoopInput()

        return { "GW4x90ADC": marshal(adcValues, gw4x90adc_fields) }, 200

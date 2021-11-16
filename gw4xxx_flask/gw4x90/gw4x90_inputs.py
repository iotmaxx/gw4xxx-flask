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
from gw4xxx_hal.gw4x90 import digitalInputControl
import os

num_inputs = 2

input_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4x90_gpi', absolute=True)
}


class GW4x90GPI(Resource):
    def __init__(self):
        self.values = { "values" : num_inputs*[ False ] }
        super(GW4x90GPI, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'inputs':  marshal(self.values, input_fields) }

    def _selfGetInputs(self):
        for inp in range(num_inputs):
            self.values["values"][inp] = digitalInputControl.getInput(inp) != 0

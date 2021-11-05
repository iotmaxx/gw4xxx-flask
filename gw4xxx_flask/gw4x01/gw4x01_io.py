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
from gw4xxx_hal.gw4x01 import digitalIOControl
import os

input_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4x01_gpi', absolute=True)
}

isoin_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4x01_isoin', absolute=True)
}

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    theIsoIns = [
        digitalIOControl.GW4x01IsoInput(0),
        digitalIOControl.GW4x01IsoInput(1),
        digitalIOControl.GW4x01IsoInput(2),
        digitalIOControl.GW4x01IsoInput(3)
    ]
    theInputs = [
        digitalIOControl.GW4x01Input(0),
        digitalIOControl.GW4x01Input(1),
        digitalIOControl.GW4x01Input(2),
        digitalIOControl.GW4x01Input(3)
    ]


class GW4x01GPI(Resource):
    def __init__(self):
        self.values = { "values" : len(theInputs)*[ False ] }
        super(GW4x01GPI, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'inputs':  marshal(self.values, input_fields) }

    def _selfGetInputs(self):
        for inp in range(len(theInputs)):
            self.values["values"][inp] = theInputs[inp].getInput() != 0

class GW4x01IsoIn(Resource):
    def __init__(self):
        self.values = { "values" : len(theIsoIns)*[ False ] }
        super(GW4x01IsoIn, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'isoins':  marshal(self.values, isoin_fields) }

    def _selfGetInputs(self):
        for inp in range(len(theIsoIns)):
            self.values["values"][inp] = theIsoIns[inp].getInput() != 0


class GW4x01IsoOut(Resource):
    def get(self, id):
         return { 'api' : 'GW4x01IsoOut' }

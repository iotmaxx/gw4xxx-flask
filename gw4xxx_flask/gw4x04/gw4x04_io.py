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
from gw4xxx_hal.gw4x04 import digitalIOControl
from gw4xxx_flask.app import theApplication

import os

input_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4x04_gpi', absolute=True)
}

isoin_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4x04_isoin', absolute=True)
}

isoout_fields = {
    "id":       fields.Integer,
    "value":    fields.Boolean,
    'uri':      fields.Url('gw4x04_isoout', absolute=True)
}

#if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
if (not theApplication.debug) or os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get('SERVER_SOFTWARE') is not None:
    theIsoOuts = [
        digitalIOControl.GW4x04IsoOutput(0),
        digitalIOControl.GW4x04IsoOutput(1),
    ]
    theIsoIns = [
        digitalIOControl.GW4x04IsoInput(0),
        digitalIOControl.GW4x04IsoInput(1),
        digitalIOControl.GW4x04IsoInput(2),
        digitalIOControl.GW4x04IsoInput(3)
    ]
    theInputs = [
        digitalIOControl.GW4x04Input(0),
        digitalIOControl.GW4x04Input(1),
        digitalIOControl.GW4x04Input(2),
        digitalIOControl.GW4x04Input(3)
    ]


class GW4x04GPI(Resource):
    def __init__(self):
        self.values = { "values" : len(theInputs)*[ False ] }
        super(GW4x04GPI, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'inputs':  marshal(self.values, input_fields) }

    def _selfGetInputs(self):
        for inp in range(len(theInputs)):
            self.values["values"][inp] = theInputs[inp].getInput() != 0

class GW4x04IsoIn(Resource):
    def __init__(self):
        self.values = { "values" : len(theIsoIns)*[ False ] }
        super(GW4x04IsoIn, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'isoins':  marshal(self.values, isoin_fields) }

    def _selfGetInputs(self):
        for inp in range(len(theIsoIns)):
            self.values["values"][inp] = theIsoIns[inp].getInput() != 0

class GW4x04IsoOut(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('state', type = inputs.boolean, required = True,
            help = 'no state provided', location = 'json')
        super(GW4x04IsoOut, self).__init__()

    def get(self, id):
        if id>=len(theIsoOuts):
            abort(404)
#        return { 'isoout':  marshal({ 'value': theIsoOuts[0].getOutput()!=0, 'id': 0 }, isoout_fields) }
        return { 'isoout':  marshal({ 'value': theIsoOuts[id].getOutput()!=0, 'id': id }, isoout_fields) }

    def put(self, id):
        if id>=len(theIsoOuts):
            abort(404)
        args = self.putparse.parse_args()
        theIsoOuts[id].setOutput(args['state'])
        return { 'isoout':  marshal({ 'value': theIsoOuts[id].getOutput()!=0, 'id': id }, isoout_fields) }

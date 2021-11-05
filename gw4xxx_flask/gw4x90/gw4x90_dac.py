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

import os

class GW4x90DAC(Resource):
    def get(self, chip, channel):
        return { "GW4x90DAC" : "Chip: {}, Channel: {}".format(chip, channel) }
#         if id>=len(theIsoOuts):
#             abort(404)
# #        return { 'isoout':  marshal({ 'value': theIsoOuts[0].getOutput()!=0, 'id': 0 }, isoout_fields) }
#         return { 'isoout':  marshal({ 'value': theIsoOuts[id].getOutput()!=0, 'id': id }, isoout_fields) }

    # def put(self, id):
    #     if id>=len(theIsoOuts):
    #         abort(404)
    #     args = self.putparse.parse_args()
    #     theIsoOuts[id].setOutput(args['state'])
    #     return { 'isoout':  marshal({ 'value': theIsoOuts[id].getOutput()!=0, 'id': id }, isoout_fields) }

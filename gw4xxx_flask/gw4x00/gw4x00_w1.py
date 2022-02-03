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
from flask_restful import Resource, fields, marshal, reqparse, inputs

w1DevicesDir = "/sys/bus/w1/devices/"
w1SlaveNumberFile = w1DevicesDir+"w1_bus_master1/w1_master_slave_count"
w1SlaveListFile = w1DevicesDir+"w1_bus_master1/w1_master_slaves"

gw4100w1device_fields = {
    "id": fields.Integer,
    "w1-id": fields.String, 
    "uri": fields.Url('gw4100_w1device', absolute=True)
}

gw4100w1devices_fields = {
    "num": fields.Integer,
    "devices": fields.List(fields.Nested(gw4100w1device_fields)),
    "uri": fields.Url('gw4100_w1', absolute=True)
}


class GW4x00W1(Resource):
    def __init__(self):
        self.devices = self._getDevices()
        self.theDevices = {
            "num": len(self.devices),
            "devices": []
        }
#        for idx in len(self.devices):

        super(GW4x00W1, self).__init__()

    def _getDevices(self):
        with open(w1SlaveNumberFile, "r") as f:
            numDevices = int(f.read()) 
        if numDevices==0:
            return []
        with open(w1SlaveListFile, "r") as f:
            return f.read().splitlines()

    def get(self):
#        self._selfGetInputs()
        return { 'w1':  marshal(self.theDevices, gw4100w1devices_fields) }

class GW4x00W1DEV(Resource):
    def get(self, id):
#        self._selfGetInputs()
        return { 'w1dev':  id }

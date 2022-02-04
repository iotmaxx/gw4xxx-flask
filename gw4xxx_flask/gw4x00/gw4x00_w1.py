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
w1TemperatureFile = "temperature"
w1AlarmsFile = "alarms"
w1ResolutionFile = "resolution"
w1ExtPowerFile = "ext_power"

gw4100w1device_fields = {
    "id": fields.Integer,
    "serial": fields.String, 
    "uri": fields.Url('gw4100_w1device', absolute=True)
}

gw4100w1devices_fields = {
    "num": fields.Integer,
    "devices": fields.List(fields.Nested(gw4100w1device_fields)),
    "uri": fields.Url('gw4100_w1', absolute=True)
}

gw4100w1temperature_fields = {
    'temperature': fields.Float, 
    'alarms': fields.List(fields.Integer), 
    'resolution': fields.Integer, 
    'ext_power': fields.Boolean
}

def getDevices():
    with open(w1SlaveNumberFile, "r") as f:
        numDevices = int(f.read()) 
    if numDevices==0:
        return []
    with open(w1SlaveListFile, "r") as f:
        return f.read().splitlines()

def getTemperature(owid):
    with open(w1DevicesDir+owid+"/"+w1TemperatureFile, "r") as f:
        return round(float(f.read()) / 1000.0, 2)

def getAlarms(owid):
    with open(w1DevicesDir+owid+"/"+w1AlarmsFile, "r") as f:
        return f.read().split()

def getResolution(owid):
    with open(w1DevicesDir+owid+"/"+w1ResolutionFile, "r") as f:
        return int(f.read())

def getExtPower(owid):
    with open(w1DevicesDir+owid+"/"+w1ExtPowerFile, "r") as f:
        return int(f.read()) == 1

class GW4x00W1(Resource):
    def __init__(self):
        self.devices = getDevices()
        self.theDevices = {
            "num": len(self.devices),
            "devices": []
        }
        for idx, device in enumerate(self.devices):
            theDevice = {
                "id": idx,
                "serial": device
            }
            self.theDevices["devices"].append(theDevice)

        super(GW4x00W1, self).__init__()

    def get(self):
#        self._selfGetInputs()
        return marshal(self.theDevices, gw4100w1devices_fields), 200

class GW4x00W1DEV(Resource):
    def get(self, id):
#        self._selfGetInputs()
        device_fields = gw4100w1device_fields.copy()
        device_fields['type'] = fields.String
        theDevice  = {
            'id': id,
            'serial':  getDevices()[id],
            'type': 'unsupported'
        }
        devFamily = theDevice['serial'].split("-",1)[0]

        if(devFamily == '28'):
            device_fields['values'] = fields.Nested(gw4100w1temperature_fields)
            theTemperatureSensor = {
                'temperature': getTemperature(theDevice['serial']), 
                'alarms': getAlarms(theDevice['serial']), 
                'resolution': getResolution(theDevice['serial']), 
                'ext_power': getExtPower(theDevice['serial'])
            }
            theDevice['type'] = 'temperature'
            theDevice['values'] = theTemperatureSensor

        return marshal(theDevice, device_fields), 200

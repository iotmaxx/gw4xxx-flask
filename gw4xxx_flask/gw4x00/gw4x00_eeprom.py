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
from gw4xxx_flask.app import theApi, theApplication, reqparser
from gw4xxx_hal.gw4xxx import gw4xxx_eeprom
from gw4xxx_flask.app.formats import dateFormat

import os

boardData_fields = {
    "Product"           : fields.Integer,
    "ProductName"       : fields.String,
    "SerialNumber"      : fields.String,
    "Version"           : fields.List(fields.Integer),
    "Manufacturer"      : fields.Integer,
#    "TimeOfProduction"  : fields.DateTime(dt_format='iso8601'),
#    "TimeOfProduction"  : fields.Integer,
    "TimeOfProduction"  : dateFormat,
    "Tester"            : fields.Integer,
    "TestResult"        : fields.Integer,
 #   "TimeOfTest"        : fields.DateTime(dt_format='iso8601'),
#    "TimeOfTest"        : fields.Integer,
    "TimeOfTest"        : dateFormat,
}

mainBoardData_fields = boardData_fields.copy()
mainBoardData_fields["MAC"] = fields.List(fields.Integer)
mainBoardData_fields["uri"] = fields.Url('gw4100', absolute=True)

expansionBoard_fields = boardData_fields.copy()
expansionBoard_fields["OverlayName"] = fields.String
  
class MainBoardEEPROM(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('Product', type = reqparser.int_range(min=0, max=0xff), store_missing=False)
        self.putparse.add_argument('ProductName', store_missing=False)
        self.putparse.add_argument('SerialNumber', store_missing=False),
        self.putparse.add_argument('Version', type = reqparser.version(), store_missing=False)
        self.putparse.add_argument('Manufacturer', type = reqparser.int_range(min=0, max=0xff), store_missing=False)
        self.putparse.add_argument('TimeOfProduction', type = reqparser.timestamp(), store_missing=False)
        self.putparse.add_argument('Tester', type = reqparser.int_range(min=0, max=0xff), store_missing=False)
        self.putparse.add_argument('TestResult', type = reqparser.int_range(min=0, max=0xff), store_missing=False)
        self.putparse.add_argument('TimeOfTest', type = reqparser.timestamp(), store_missing=False)
        self.putparse.add_argument('OverlayName', store_missing=False)
        self.putparse.add_argument('MAC', type = reqparser.MACAddress(), store_missing=False)
        
        super(MainBoardEEPROM, self).__init__()

    def get(self, board):
        if board == 'gw4x00':
            return marshal(gw4xxx_eeprom.readDeviceData()['Main'], mainBoardData_fields), 200
        elif board == 'gw4x01':
            return marshal(gw4xxx_eeprom.readDeviceData()['Expansion'], expansionBoard_fields), 200
        else:
            return {'error': 'not found'}, 404

    def put(self, board):
        args = self.putparse.parse_args()
        print(f"put Board: {board}")
        if board == 'gw4x00':
            if "MAC" in args:
                specificSection = {}
                specificSection['MAC'] = args.pop('MAC')
                gw4xxx_eeprom.writeMainBoardEEPROM(args, specificSection)
            else:
                gw4xxx_eeprom.writeMainBoardEEPROM(args)
            return marshal(gw4xxx_eeprom.readDeviceData()['Main'], mainBoardData_fields), 200
        elif board == 'gw4x01':
            print("Write to expansion board")
            gw4xxx_eeprom.writeExpansionBoardEEPROM(args)
            return marshal(gw4xxx_eeprom.readDeviceData()['Expansion'], expansionBoard_fields), 200
        else:
            return {'error': 'not found'}, 404


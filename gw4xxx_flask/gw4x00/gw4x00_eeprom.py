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
from app import theApi, theApplication, reqparser
from gw4xxx_hal.gw4x90 import analogIOControl
import os



class MainBoardEEPROM(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('Product', type = reqparser.int_range(min=0, max=0xff))
        self.putparse.add_argument('ProductName')
        self.putparse.add_argument('SerialNumber'),
        self.putparse.add_argument('Version', type = reqparser.version())
        self.putparse.add_argument('Manufacturer', type = reqparser.int_range(min=0, max=0xff))
        self.putparse.add_argument('TimeOfProduction', type = reqparser.int_range(min=0, max=0xffffffff))
        self.putparse.add_argument('Tester', type = reqparser.int_range(min=0, max=0xff))
        self.putparse.add_argument('TestResult', type = reqparser.int_range(min=0, max=0xff))
        self.putparse.add_argument('TimeOfTest', type = reqparser.int_range(min=0, max=0xffffffff))
        self.putparse.add_argument('OverlayName')
        super(MainBoardEEPROM, self).__init__()

    def put(self):
        args = self.putparse.parse_args()
        return { 'MainBoardEEPROM': args }


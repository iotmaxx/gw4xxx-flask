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

class GW4x01RTD(Resource):
    def get(self):
         return { 'api' : 'GW4x01RTD' }

class GW4x01CurrentLoopIn(Resource):
    def get(self):
         return { 'api' : 'GW4x01CurrentLoopIn' }

class GW4x01CurrentLoopOut(Resource):
    def get(self):
         return { 'api' : 'GW4x01CurrentLoopOut' }

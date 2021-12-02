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
""" 
from flask_restful import ValidationError

def min_length(min_length):
    def validate(s):
        if len(s) >= min_length:
            return s
        raise ValidationError("String must be at least %i characters long" % min)
    return validate

def int_in_range(upper, lower=0):
    def validate(s):
        if s >= lower and s <= upper:
            return s
        raise ValidationError("%i not in range [%i..%i]" % s, lower, upper)
    return validate
 """
import json
import datetime
import dateutil.parser as dp

def float_range(min=0, max=255):
    def validate(value):
        theFloat = float(value)
        if min <= theFloat <= max:
            return value
        raise ValueError(f"Value must be in range [{min}, {max}]")

    return validate

def int_range(min=0, max=255):
    def validate(value):
#        print("validate float range for {}".format(value))
        theInt = int(value)
        if min <= theInt <= max:
            return value
        raise ValueError(f"Value must be in range [{min}, {max}]")

    return validate

def version():
    def validate(value):
        theList = json.loads(value)
        if isinstance(theList, list):
            if len(theList) == 3:
                for idx in range(3):
                    if not isinstance(theList[idx],int):
                        raise ValueError(f"Not int: {idx}")
                    if not 0 <= theList[idx] <= 0xff:
                        raise ValueError(f"Not in range: {idx}")
                    
                return theList
        raise ValueError(f"Version: {value}")

    return validate

def MACAddress():
    def validate(value):
        print("validate MAC {}".format(value))
        theList = json.loads(value)
        if isinstance(theList, list):
#            print("is list")
            if len(theList) == 6:
                print("is len 6")
                for idx in range(6):
                    if not isinstance(theList[idx],int):
                        raise ValueError(f"Not int: {idx}")
                    if not 0 <= theList[idx] <= 0xff:
                        raise ValueError(f"Not in range: {idx}")
                    
                return theList
        raise ValueError(f"Version: {value}")

    return validate


def timestamp():
    def validate(value):
#        print("validate float range for {}".format(value))
        theDateTime = dp.parse(value)
        theTimestamp = theDateTime.timestamp()
        return int(theTimestamp)
#        raise ValueError(f"Value must be in range [{min}, {max}]")

    return validate


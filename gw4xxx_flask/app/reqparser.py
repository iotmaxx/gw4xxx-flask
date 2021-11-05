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


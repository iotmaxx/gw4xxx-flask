import time
from flask_restful import Resource, fields, marshal, reqparse
from gw4xxx_flask.app import reqparser

import serial.rs485

input_fields = {
    "recv":         fields.String,
    "timeout":      fields.Integer,
    'timed_out':    fields.Boolean,
    'uri':          fields.Url('gw4100_rs485', absolute=True)
}

class GW4x00RS485(Resource):
    def __init__(self):
        self.getparse = reqparse.RequestParser()
        self.getparse.add_argument('timeout', type = reqparser.int_range(min=0, max=10), default=3)
        super(GW4x00RS485, self).__init__()

    def get(self):
        args = self.getparse.parse_args()
        theResponse = {}
        theResponse['recv'] = 'Hello'
        theResponse['timeout'] = args['timeout']
        theResponse['timed_out'] = False
        time.sleep(theResponse['timeout'])
        return marshal(theResponse, input_fields)

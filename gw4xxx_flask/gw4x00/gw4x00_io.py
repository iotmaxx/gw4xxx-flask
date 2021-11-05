from flask_restful import Resource, fields, marshal, reqparse, inputs
from flask import request
from gw4xxx_hal.gw4x00 import digitalIOControl
from gw4xxx_hal.gw4x00.gw4x00_interfaces import gw4x00GpioState
from app import theApplication
import os

gpios = [
    {
        "id":       0,
        "highside": False,
        "lowside":  False,
        "pullup":   False,
        "input":    False,
        "adc":      0
    },
    {
        "id":       1,
        "highside": False,
        "lowside":  False,
        "pullup":   False,
        "input":    False,
        "adc":      0
    }
]

gpio_fields = {
    "highside": fields.Boolean,
    "lowside":  fields.Boolean,
    "pullup":   fields.Boolean,
    "input":    fields.Boolean,
    "adc":      fields.Fixed(decimals=2),
    'uri':      fields.Url('gw4100_gpio', absolute=True)
}

input_fields = {
    "values":   fields.List(fields.Boolean),
    'uri':      fields.Url('gw4100_gpi', absolute=True)
}

#print("WERKZEUG_RUN_MAIN: {}, FLASK_ENV: {}, debug:{}".format(os.environ.get("WERKZEUG_RUN_MAIN"), os.environ.get("FLASK_ENV"), theApplication.debug))

#if (not os.environ.get("FLASK_ENV") == "development") or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#if not (theApplication.debug or os.environ.get("FLASK_ENV") == "development") or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    theInputs = [
        digitalIOControl.GW4100CounterInput(0),
        digitalIOControl.GW4100CounterInput(1),
        digitalIOControl.GW4100CounterInput(2),
        digitalIOControl.GW4100CounterInput(3)
    ]
    theGpios = [
        digitalIOControl.GW4100Gpio(0),
        digitalIOControl.GW4100Gpio(1),
    ]

class GW4x00GPI(Resource):
    def __init__(self):
#        self.inputValues = len(theInputs)*[]
#        self.values = { "values" : [ False, False, False, False ] }
        self.values = { "values" : len(theInputs)*[ False ] }
        super(GW4x00GPI, self).__init__()

    def get(self):
        self._selfGetInputs()
        return { 'inputs':  marshal(self.values, input_fields) }

    def _selfGetInputs(self):
        for inp in range(len(theInputs)):
            self.values["values"][inp] = theInputs[inp].getInput() != 0

def gpiostate(gpiostate_str):
    print(gpiostate_str)
    if gpiostate_str in gw4x00GpioState:
        return gpiostate_str
    else:
        raise ValueError('{} is not a valid GPIO status'.format(gpiostate_str))

class GW4x00GPIO(Resource):
    def __init__(self):
        self.putparse = reqparse.RequestParser()
        self.putparse.add_argument('state', type = gpiostate, required = True,
            help = 'Invalid or no state provided', location = 'json')
        self.putparse.add_argument('pullup', type = inputs.boolean, location = 'json')
        super(GW4x00GPIO, self).__init__()

    def get(self, id):
        self._updateGpios(id)
        return { 'gpio':  marshal(gpios[id], gpio_fields) }

    def put(self, id):
        args = self.putparse.parse_args()
        theGpios[id].setOutput(args['state'])
        if args['pullup'] != None:
            theGpios[id].activatePullup(bool(args['pullup']))                        
        self._updateGpios(id)
        return { 'gpio':  marshal(gpios[id], gpio_fields) }

    def _updateGpios(self, id):
        for output in [ "highside", "lowside", "pullup"]:
            gpios[id][output] = theGpios[id].getOutput(output) != 0
        gpios[id]["input"] = theGpios[id].getInput() != 0
        gpios[id]["adc"] = theGpios[id].getADC() 

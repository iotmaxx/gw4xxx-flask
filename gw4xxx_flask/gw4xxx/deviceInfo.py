from flask_restful import Resource, fields, marshal
from gw4xxx_hal.gw4xxx import gw4xxx_eeprom
from datetime import datetime

class MyDateFormat(fields.Raw):
    def format(self, value):
        return datetime.fromtimestamp(value).isoformat()
#        value.strftime('%Y-%m-%d')


boardData_fields = {
    "Product"           : fields.Integer,
    "ProductName"       : fields.String,
    "SerialNumber"      : fields.String,
    "Version"           : fields.List(fields.Integer),
    "Manufacturer"      : fields.Integer,
#    "TimeOfProduction"  : fields.DateTime(dt_format='iso8601'),
#    "TimeOfProduction"  : fields.Integer,
    "TimeOfProduction"  : MyDateFormat,
    "Tester"            : fields.Integer,
    "TestResult"        : fields.Integer,
 #   "TimeOfTest"        : fields.DateTime(dt_format='iso8601'),
#    "TimeOfTest"        : fields.Integer,
    "TimeOfTest"        : MyDateFormat,
}

mainBoardData_fields = boardData_fields.copy()
mainBoardData_fields["MAC"] = fields.List(fields.Integer)

expansionBoard_fields = boardData_fields.copy()
expansionBoard_fields["OverlayName"] = fields.String

info_fields = {
    "device":       fields.String,
    "Main":         fields.Nested(mainBoardData_fields),
    'uri':          fields.Url('gw4xxx_deviceInfo')
}

theData0 = {
    "Product" : 0,
    "ProductName" : "ProductName0",
    "SerialNumber" : "Serial0",
    "Version" : [ 1, 2, 3 ],
    "Manufacturer" : 0,
    "TimeOfProduction" : 0,
    "Tester" : 0,
    "TestResult" : 0,
    "TimeOfTest" : 0,
    "OverlayName" : "None"
}

theData1 = {
    "Product" : 1,
    "ProductName" : "ProductName1",
    "SerialNumber" : "Serial1",
    "Version" : [ 4, 5, 6 ],
    "Manufacturer" : 1,
    "TimeOfProduction" : 1,
    "Tester" : 1,
    "TestResult" : 1,
    "TimeOfTest" : 1,
    "OverlayName" : "Some"
}

theTestData = {
    "device": "theDevice",
    "boards": [theData0, None]
}

class DeviceInfoAPI(Resource):
    def get(self):
        deviceData = gw4xxx_eeprom.readDeviceData()
        if 'Expansion' in deviceData:
            info_fields["Expansion"] = fields.Nested(expansionBoard_fields)
        return marshal(deviceData, info_fields), 200

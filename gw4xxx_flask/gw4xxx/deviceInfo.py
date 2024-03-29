from flask_restful import Resource, fields, marshal
from gw4xxx_hal.gw4xxx import gw4xxx_eeprom, halVersion, system
from datetime import datetime
from gw4xxx_flask.app import theApi, apiVersion
from gw4xxx_flask.app.formats import dateFormat
from gw4xxx_flask.gw4x00.gw4x00_eeprom import MainBoardEEPROM

#theApi.add_resource(MainBoardEEPROM, '/gw4x00/eeprom/<board>', endpoint='gw4x00_eeprom')
theApi.add_resource(MainBoardEEPROM, '/<board>/eeprom', endpoint='gw4x00_eeprom')

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

softwareVersionData_fields = {
    "hal": fields.String,
    "api": fields.String,
}

systemInfoData_fields = {
    "imx7_socid":   fields.String,
    "IMEI":         fields.String,
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

deviceData = gw4xxx_eeprom.readDeviceData()
if deviceData['Main']['ProductName'][0:4] == 'GW41':
    from gw4xxx_flask.gw4x00.gw4100 import GW4100API
    theApi.add_resource(GW4100API, '/gw4100', endpoint='gw4100')
    mainBoardData_fields = boardData_fields.copy()
    mainBoardData_fields["MAC"] = fields.List(fields.Integer)
    mainBoardData_fields["uri"] = fields.Url('gw4100', absolute=True)
elif deviceData['Main']['ProductName'] == 'Unknown':
    from gw4xxx_flask.gw4x00.gw4100 import GW4100API
    theApi.add_resource(GW4100API, '/gw4100', endpoint='gw4100')
    mainBoardData_fields = boardData_fields.copy()
    mainBoardData_fields["MAC"] = fields.List(fields.Integer)
    mainBoardData_fields["uri"] = fields.Url('gw4100', absolute=True)
else:
    print("should not happen")

info_fields = {
    "device":       fields.String,
    "Software":     fields.Nested(softwareVersionData_fields),
    "System":       fields.Nested(systemInfoData_fields),
    "Main":         fields.Nested(mainBoardData_fields),
    'uri':          fields.Url('gw4xxx_deviceInfo', absolute=True)
}

if 'Expansion' in deviceData:
    expansionBoard_fields = boardData_fields.copy()
    expansionBoard_fields["OverlayName"] = fields.String
    if deviceData['Expansion']['ProductName'][-2:] == '01':
        from gw4xxx_flask.gw4x01.gw4x01 import GW4x01API
        theApi.add_resource(GW4x01API, '/gw4x01', endpoint='gw4x01')
        expansionBoard_fields["uri"] = fields.Url('gw4x01', absolute=True)
    elif deviceData['Expansion']['ProductName'][-2:] == '02':
        from gw4xxx_flask.gw4x02.gw4x02 import GW4x02API
        theApi.add_resource(GW4x02API, '/gw4x02', endpoint='gw4x02')
        expansionBoard_fields["uri"] = fields.Url('gw4x02', absolute=True)
    elif deviceData['Expansion']['ProductName'][-2:] == '04':
        from gw4xxx_flask.gw4x04.gw4x04 import GW4x04API
        theApi.add_resource(GW4x04API, '/gw4x04', endpoint='gw4x04')
        expansionBoard_fields["uri"] = fields.Url('gw4x04', absolute=True)
    # todo: correct tester id to 4x90
    if deviceData['Expansion']['ProductName'][-2:] == '99' or deviceData['Expansion']['ProductName'][-2:] == '90' :
        from gw4xxx_flask.gw4x90.gw4x90 import GW4x90API
        theApi.add_resource(GW4x90API, '/gw4x90', endpoint='gw4x90')
        expansionBoard_fields["uri"] = fields.Url('gw4x90', absolute=True)
    info_fields["Expansion"] = fields.Nested(expansionBoard_fields)

deviceData['Software'] = {}
deviceData['Software']['hal'] = halVersion
deviceData['Software']['api'] = apiVersion

#deviceData['System'] = {}
#deviceData['System']['socid'] = 'test'


class DeviceInfoAPI(Resource):
    def get(self):
        deviceData.update(gw4xxx_eeprom.readDeviceData())
        deviceData['System'] = system.getSystemInfo()
        return marshal(deviceData, info_fields), 200

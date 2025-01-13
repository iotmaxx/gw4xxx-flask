from flask_restful import Resource, fields, marshal
from gw4xxx_flask.app import theApi, apiVersion

from sdhealth.sdhealth import getSDHealth, UNSUPPORTED_CARD_ERROR

sdcard_fields = {
    "FlashID": fields.List(fields.Integer),
    "ICVersion": fields.Integer,
    "FWVersion": fields.Integer,
    "CENumber": fields.Integer,
    "BadBlockReplaceMaximum": fields.Integer,
    "BadBlockcountperDie": fields.List(fields.Integer),
    "GoodBlockRatePerCent": fields.Float,
    "TotalEraseCount": fields.Integer,
    "EnduranceRemainLifePerCent": fields.Float,
    "AverageEraseCountL": fields.Integer,
    "MinimumEraseCountL": fields.Integer,
    "MaximumEraseCountL": fields.Integer,
    "AverageEraseCountH": fields.Integer,
    "MinimumEraseCountH": fields.Integer,
    "MaximumEraseCountH": fields.Integer,
    "PowerUpCount": fields.Integer,
    "AbnormalPowerOffCount": fields.Integer,
    "TotalRefreshCount": fields.Integer,
    'uri':          fields.Url('gw4100_sdhealth', absolute=True)
}

class SDCardHealth(Resource):
    def get(self):
        try:
            sdHealthData = getSDHealth()
            print(sdHealthData)
            return marshal(sdHealthData, sdcard_fields), 200
        except FileNotFoundError:
            return {'error': 'SD card not available'}, 404
        except UNSUPPORTED_CARD_ERROR:
            return {'error': 'SD card health status not supported'}, 415
        except Exception as e:
            print(type(e))
            print(e)
            return {'error': 'internal error'}, 500

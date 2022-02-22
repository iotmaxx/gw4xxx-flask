from gw4xxx_flask.version import __version__

serviceDescription = "Flask Webservice on HAL"
serviceFile = "/config/iot_launcher.d/flaskonhal.json"

defaultService = {
    "FlaskOnHAL": {
        "application": "gunicorn --bind 0.0.0.0:5000 gw4xxx_flask:theApplication".split(), 
        "configFile": None, 
        "version":  __version__,
        "description": serviceDescription, 
        "type": "test application", 
        "publisher": {
            "name": "IoTmaxx GmbH", 
            "URL": "www.iotmaxx.de"
        }
    }
}

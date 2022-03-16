from flask import Flask
from flask_restful import Api, Resource

apiVersion = "0.1.4"
theApplication = Flask(__name__)
#theApplication.config['SERVER_NAME'] = '192.168.1.1:5000'
theApi = Api(theApplication)

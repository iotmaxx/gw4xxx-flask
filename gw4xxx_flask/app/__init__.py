from flask import Flask

theApplication = Flask(__name__)

from app import routes


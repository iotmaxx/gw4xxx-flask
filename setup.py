from setuptools import setup, find_packages
#import gwmqtt.default_config as defCfg
#import json

version = {}
with open("gw4xxx_flask/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='gw4xxx_flask',
    version=version['__version__'],
    url='https://github.com/iotmaxx/gw4xxx-flask',
    author='Ralf Glaser',
    author_email='glaser@iotmaxx.de',
    description='flask service on top of gw4xxx_hal',
    packages=find_packages(),    
    install_requires=[],
)

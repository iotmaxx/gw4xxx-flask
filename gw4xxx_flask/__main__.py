from gw4xxx_flask.app import theApplication
import gw4xxx_flask.app.wsgi

if __name__ == '__main__':
    theApplication.run(host='0.0.0.0',debug=True)
    

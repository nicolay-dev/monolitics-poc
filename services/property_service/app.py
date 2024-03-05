from flask import Flask
from entrypoints.rest.api_rest import app

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)
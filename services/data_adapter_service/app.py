
from flask import Flask
from services.data_adapter_service.entrypoints.api_rest import app

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)
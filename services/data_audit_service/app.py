
from flask import Flask
from services.data_audit_service.entrypoints.api_rest import app
import pulsar


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)
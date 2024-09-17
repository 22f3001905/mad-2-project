import json

from flask import make_response
from werkzeug.exceptions import HTTPException

class NotFoundError(HTTPException):
    def __init__(self, status_code=404, error_message="Not found."):
        message = {
            "status_code": status_code,
            "error_message": error_message
        }

        self.response = make_response(json.dumps(message), status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        message = {
            "status_code": status_code,
            "error_message": error_message
        }

        self.response = make_response(json.dumps(message), status_code)

class DuplicateDataFoundError(HTTPException):
    def __init__(self, status_code=403, error_message="Duplicate data found."):
        message = {
            "status_code": status_code,
            "error_message": error_message
        }

        self.response = make_response(json.dumps(message), status_code)

class IncompleteDataProvidedError(HTTPException):
    def __init__(self, status_code=403, error_message="Incomplete data provided."):
        message = {
            "status_code": status_code,
            "error_message": error_message
        }

        self.response = make_response(json.dumps(message), status_code)

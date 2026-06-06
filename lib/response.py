from flask import jsonify


def respond_success(data, message="Success", status=200):
    return jsonify({"message": message, "data": data}), status


def respond_error(message, error="Error", details=None, status=400):
    body = {"message": message, "error": error}
    if details is not None:
        body["details"] = details
    return jsonify(body), status

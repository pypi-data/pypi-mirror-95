from jsonschema import validate

from superwise.exceptions.superwise_exceptions import SuperwiseRequestFormatError


def valid_trace_prediction_emit(data):
    """
    validate trace request from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "record": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "ts": {"format": "date-time"},
                    "features": {
                        "type": "object"
                    },
                    "prediction_value": {"type": ["string", "number"]},
                    "prediction_probability": {"type": "number"},
                    "label_weight": {"type": "number"}
                },
                "required": ["id", "ts", "features"],
                "additionalProperties": False
            },
            "version_id": {"type": "string"},
        },
        "required": ["record", "version_id"],
        "additionalProperties": False
    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception as e:
        raise SuperwiseRequestFormatError(f"Request not in the right format with error {e}")


def valid_trace_prediction_batch(data):
    """
    validate trace batch requests from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string"
                            },
                            "ts": {"format": "date-time"},
                            "features": {
                                "type": "object"
                            },
                            "prediction_value": {
                                "type": ["string", "number","null"]
                            },
                            "prediction_probability": {
                                "type": ["number","null"]
                            },
                            "label_weight": {
                                "type": ["number", "null"]
                            },
                        },
                        "required": [
                            "id",
                            "ts",
                            "features"
                        ],
                        "additionalProperties": False
                    }
                ]
            },
            "version_id": {
                "type": "string"
            },
            "category": {
                "type": "string"
            }
        },
        "required": [
            "records", "version_id"
        ],
        "additionalProperties": False

    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception:
        raise SuperwiseRequestFormatError("Request not in the right format...")


def valid_trace_prediction_file(data):
    """
    validate trace request from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "file_url": {"type": "string"},
            "version_id": {"type": "string"}
        },
        "required": ["file_url", "version_id"],
        "additionalProperties": False
    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception:
        raise SuperwiseRequestFormatError("Request not in the right format...")


def valid_trace_label_emit(data):
    """
    validate trace request from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "ts": {"format": "date-time"},
            "label": {"type": ["string", "number"]},
        },
        "required": ["id", "ts", "label"],
        "additionalProperties": False
    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception:
        raise SuperwiseRequestFormatError("Request not in the right format...")


def valid_trace_label_batch(data):
    """
    validate trace batch requests from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string"
                            },
                            "ts": {"format": "date-time"},
                            "label": {
                                "type": ["string", "number"]
                            },

                        },
                        "required": [
                            "id",
                            "ts",
                            "label",
                        ],
                        "additionalProperties": False
                    }
                ]
            },
            "category": {
                "type": "string"
            }
        },
        "required": [
            "records"
        ],
        "additionalProperties": False
    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception:
        raise SuperwiseRequestFormatError("Request not in the right format...")


def valid_trace_label_file(data):
    """
    validate trace request from user
    :param data:
    :return: return if the data format is valid or not
    """
    schema = {
        "type": "object",
        "properties": {
            "file_url": {"type": "string"}
        },
        "required": ["file_url"],
        "additionalProperties": False
    }
    try:
        res = validate(instance=data, schema=schema)
        return res is None
    except Exception:
        raise SuperwiseRequestFormatError("Request not in the right format...")

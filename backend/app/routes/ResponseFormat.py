import json
from flask import Response


def responseFormat(element):
    return Response(
        json.dumps(element, sort_keys=False, indent=2),
        mimetype='application/json'
    )
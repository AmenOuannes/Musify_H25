import json
from flask import Response


def responseFormat(element):
    return Response(
        json.dumps(element, sort_keys=False, indent=2),
        mimetype='application/json'
    )

def usernames_response(all_users):
    return [{'username':user['username']} for user in all_users]
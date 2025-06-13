import json

import xbmc

def jsonrpc_request(method: str, params=None):
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }

    if params is not None:
        request["params"] = params

    request_json = json.dumps(request)

    xbmc.log("Sending JSON-RPC request: {}".format(request_json), level=xbmc.LOGDEBUG)
    response_json = xbmc.executeJSONRPC(request_json)
    xbmc.log("Response from JSON-RPC request: {}".format(response_json), level=xbmc.LOGDEBUG)

    return json.loads(response_json).get("result", {})

import base64
import json


def cloud_function(request, event):
    data = json.loads(base64.b64decode(request['data']))

    # do something with `data`



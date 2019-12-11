import base64
import datetime
import json

import requests
from bs4 import BeautifulSoup
from google.cloud import datastore


def load_page(event, context):
    data = json.loads(base64.b64decode(event['data']))
    result = load_it(data['url'], data.get('param'), data['selector'])

    client = datastore.Client()

    entity = datastore.Entity(
        key=client.key('WorkResult', namespace="Archive"),
        exclude_from_indexes=('text', 'param', 'selector', 'url')
    )
    entity.update(data)
    entity.update(
        text=result,
        created_at=datetime.datetime.utcnow()
    )
    client.put(entity)


def load_it(url, param, selector):
    r1 = requests.get(url, params=param)
    soup = BeautifulSoup(r1.text, 'html.parser')
    return "".join(
        node.prettify()
        for node in soup.select(selector)
    )



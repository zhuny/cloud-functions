import json
import os

from google.cloud import datastore, pubsub_v1
from google.cloud.datastore import Key


def spead_work(event, context):
    # load from datastore
    client = datastore.Client()
    query = client.query(
        namespace="Archive",
        kind="Work"
    )

    # publish to pubsub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(
        project=client.project,
        topic=os.environ['ARCHIVE_WORK_TOPIC']
    )

    for work in query.fetch():
        info = {
            'url': work['url'],
            'param': work.get('param', {}),
            'selector': work['selector'],
            'key': work.key.id
        }
        publisher.publish(
            topic_path,
            json.dumps(info).encode()
        )


if __name__ == '__main__':
    os.environ['ARCHIVE_WORK_TOPIC'] = "archive-work"
    spead_work(None, None)



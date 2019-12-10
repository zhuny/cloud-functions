import base64
import json
import os
import requests


def cloud_build_noti(request, event):
    result = json.loads(base64.b64decode(request['data']))
    print(request)
    print(event)
    print(result)
    msg_template = (
        "*Google Cloud Build*\n"
        "Project : [{projectId}]({logUrl})\n"
        "Repository : [{substitutions[REPO_NAME]}]({substitutions[_HEAD_REPO_URL]})\n"
        "[PR#{substitutions[_PR_NUMBER]}]({substitutions[_HEAD_REPO_URL]}/pull/{substitutions[_PR_NUMBER]}) : *{substitutions[_BASE_BRANCH]} <- {substitutions[BRANCH_NAME]}#{substitutions[SHORT_SHA]}*\n"
        "Status : *{status}*"
    )
    msg = msg_template.format(**result)

    telegram_url_template = "https://api.telegram.org/bot{token}/{method}"
    telegram_url = telegram_url_template.format(
        token=os.environ['TELEGRAM_BOT_TOKEN'],
        method="sendMessage"
    )

    r1 = requests.post(
        telegram_url,
        json={
            'chat_id': int(os.environ['TELEGRAM_BOT_CHAT_ID']),
            'text': msg,
            'parse_mode': "Markdown"
        }
    )

    return r1.json()

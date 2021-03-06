import base64
import json
import os
import requests


class MsgCollectionTemplate:
    # PR 생성될 때
    trigger_by_pr = (
        "*Google Cloud Build*\n"
        "Project : <{logUrl}|{projectId}>\n"
        "Repository : <{substitutions[_HEAD_REPO_URL]}|{substitutions[REPO_NAME]}>\n"
        "<{substitutions[_HEAD_REPO_URL]}/pull/{substitutions[_PR_NUMBER]}|PR#{substitutions[_PR_NUMBER]}> : *{substitutions[_BASE_BRANCH]} <- {substitutions[BRANCH_NAME]}#{substitutions[SHORT_SHA]}*\n"
        "Status : *{status}*"
    )

    # 사실 머지라기 보다는 (마스터)브랜치 푸시 될 때
    # 그래도 _HEAD_REPO_URL는 있어야 되는거 아닌가?
    trigger_by_merge = (
        "*Google Cloud Build*\n"
        "Project : <{logUrl}|{projectId}>\n"
        "Repository : {substitutions[REPO_NAME]}\n"
        "Commit : {substitutions[BRANCH_NAME]}#{substitutions[SHORT_SHA]}\n"
        "Status : *{status}*"
    )

    # 순수하게 gcloud app deploy 할 때
    trigger_by_build = (
        "*Google Cloud Build*\n"
        "Project : <{logUrl}|{projectId}>\n"
        "Build ID : {id}\n"
        "Status : *{status}*"
    )

    @classmethod
    def get_template_list(cls):
        yield cls.trigger_by_pr
        yield cls.trigger_by_merge
        yield cls.trigger_by_build

    @classmethod
    def render(cls, result):
        for template in cls.get_template_list():
            try:
                return template.format(**result)
            except KeyError:
                # template랑 맞지 않으면 그에 맞는 폼으로 준 것이 아니라서 패스하기
                pass


def cloud_build_noti(request, event):
    result = json.loads(base64.b64decode(request['data']))
    print(request)
    print(event)
    print(result)
    msg = MsgCollectionTemplate.render(result)

    if msg is None:
        return {'status': 400}

    r1 = requests.post(
        os.environ['SLACK_WEB_HOOK_URL'],
        json={
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": msg
                    }
                }
            ]
        }
    )

    return r1.text



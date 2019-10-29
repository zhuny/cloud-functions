# 개요
Cloud Build에 트리거되는 Cloud Function

# 데이터 예시
Build가 어떤 상황에서 실행되냐에 따른 예시

* TriggerByBuild.json - `gcloud app deploy`를 실행시킬 때 생기는 Build의 정보를 가지고 있다.
* TriggerByMerge.json - 깃헙에서 push가 되는 경우가 있으면 Build가 트리거된다. 보통 PR에 의해 Master에 머지된 것이 푸시될 떄 사용된다.
* TriggerByPR.json - Pull Request가 생성되면 생기는 Build에 대한 정보를 가지고 있다.

## 구분점
`request['substitution']`에 있는 정보들로 구분할 수 있다.

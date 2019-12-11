# 구조
* Cloud Scheduler를 통해 하루에 한번, 저녁 11시에 SpreadWork를 실행
* SpreadWork에서 archive할 주소와 정보를 모아서 각 URL별로 LoadPage를 실행
* LoadPage에서 URL주소로 페이지를 불러온다.

# Storage
## WorkInfo
* url: Archive할 주소
* param: URL query 파라미터, dict()
* name: 설명

## WorkArchive
* work_id: Ref key to WorkInfo
* url: Archive할 주소
* param: URL query 파라미터, dict()
* created_at: archive한 시간
* text: 저장한 텍스트

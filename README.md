# 서울 공공데이터 공모전 백엔드

그러합니다.

## 세팅방법

### 1. firebase 세팅

`main.py` 와 같은 경로에 `firebase_cert.json` 이라는 이름으로 firebase 키 파일을 저장해주세요.
모종의 방법으로 `SEOUL_OPENDATA_KEY` 라는 이름의 환경변수에 서울시 Open API 키를 저장해주세요.

### 2. poetry 세팅

이 프로젝트는 poetry를 사용해 설정되었습니다. poetry를 설치해주세요.
이후 `main.py`가 위치한 경로로 이동해 아래 명령어를 사용해주세요.

```sh
poetry shell
```

위 명령어는 poetry 프로젝트의 가상환경을 실행해 줍니다.

```sh
poetry install
```

위 명령어는 poetry 프로젝트에 필요한 의존성 패키지들을 설치해 줍니다.

### 3. 실행

```sh
poetry run uvicorn main:app --reload
```

를 사용해 서버를 구동할 수 있습니다.

```sh
gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon
```

worker를 여러 개 구동하려면, 이 명령어로 사용해주세요.

## 그래서, 완성됬나요?

아니오. 아직 작업중이에요!!! [WIP]

## 기타 잡담

다음에 공모전을 하게 되면 초기 프로젝트 세팅할 때 poetry 쓰고... 린터랑 타입검사 깃허브 액션에 올려서 해보고싶어요...

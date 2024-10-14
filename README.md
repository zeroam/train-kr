# Train-KR

Train-KR은 한국의 고속철도 예매를 자동화하는 Python 프로젝트입니다. 현재 SRT와 KTX 예매를 지원하며, 향후 다양한 플랫폼으로 확장될 예정입니다.

## 주요 기능

- SRT 자동 예매
- KTX 자동 예매
- 원하는 시간대 지정 예약
- 예매 성공 시 Slack을 통한 알림 기능
- 다중 플랫폼 지원 (SRT, KTX)

## 설치 방법

이 프로젝트는 Poetry를 사용하여 의존성을 관리합니다. 다음 단계를 따라 설치하세요:

1. 저장소를 클론합니다:

   ```
   git clone https://github.com/your-username/train-kr.git
   cd train-kr
   ```

2. Poetry를 사용하여 의존성을 설치합니다:
   ```
   poetry install
   ```

## 사용 방법

1. `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다:

   ```
   SRT_ID=your_srt_id
   SRT_PASSWORD=your_srt_password
   KORAIL_ID=your_korail_id
   KORAIL_PW=your_korail_password
   SLACK_BOT_TOKEN=your_slack_bot_token
   ```

2. 예매 정보를 설정합니다. `srt_reservation.py` 또는 `ktx_reservation.py` 파일의 `tickets_to_reserve` 리스트를 수정하세요.

3. 스크립트를 실행합니다:
   ```
   poetry run python train-kr/srt_reservation.py
   ```
   또는
   ```
   poetry run python train-kr/ktx_reservation.py
   ```

## 프로젝트 구조

- `srt_reservation.py`: SRT 예매 로직
- `ktx_reservation.py`: KTX 예매 로직
- `slack_client.py`: Slack 알림 기능
- `config.py`: 환경 변수 설정

## 향후 계획

- SRT 다인승 예매 기능 구현
- 결제 연동 기능 구현

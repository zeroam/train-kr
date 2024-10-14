import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import settings

logger = logging.getLogger(__name__)


class SlackClient:
    def __init__(self):
        self.channel = settings.slack_channel
        self.client = WebClient(token=settings.slack_bot_token)

    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(channel=self.channel, text=message)
            logger.info(f"Message sent successfully: {response['ts']}")
        except SlackApiError as e:
            logger.error(f"Exception Raised: {e}")


# 사용 예시
if __name__ == "__main__":
    slack = SlackClient()
    slack.send_message("안녕하세요! 이것은 테스트 메시지입니다.")

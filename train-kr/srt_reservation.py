import asyncio
import logging
from SRT import SRT
from config import settings
from SRT.errors import SRTResponseError
from slack_client import SlackClient

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def reserve_ticket(
    srt: SRT,
    dep: str,
    arr: str,
    date: str,
    start_time: str,
    start_limit: str,
):
    slack_client = SlackClient() if settings.slack_bot_token else None

    while True:
        try:
            trains = await asyncio.to_thread(
                srt.search_train,
                dep=dep,
                arr=arr,
                date=date,
                time=start_time,
                time_limit=start_limit,
                available_only=False,
            )

            # 일반석만 예매
            available_trains = [
                train for train in trains if train.general_seat_available()
            ]
            logger.info(f"available trains({dep}~{arr}): {len(available_trains)}")
            if len(available_trains) == 0:
                await asyncio.sleep(1)
                continue

            reservation = await asyncio.to_thread(srt.reserve, available_trains[0])
        except SRTResponseError as e:
            logger.error(e)
            await asyncio.sleep(1)
            continue

        logger.info(f"reserver success: {reservation}")
        if slack_client:
            slack_client.send_message(f"reserve success: {reservation}")
        return reservation


async def main():
    srt_id = settings.srt_id
    srt_password = settings.srt_password

    srt = SRT(srt_id, srt_password)
    tickets_to_reserve = [
        {
            "dep": "수서",
            "arr": "부산",
            "date": "20240916",
            "start_time": "090000",
            "start_limit": "103000",
        },
        {
            "dep": "부산",
            "arr": "수서",
            "date": "20240917",
            "start_time": "190000",
            "start_limit": "210000",
        },
    ]

    tasks = [
        asyncio.create_task(reserve_ticket(srt, **ticket))
        for ticket in tickets_to_reserve
    ]
    await asyncio.gather(*tasks)

    logger.info("reserve complete!")


if __name__ == "__main__":
    asyncio.run(main())

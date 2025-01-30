import asyncio
import logging
from korail2 import (
    Korail,
    NoResultsError,
    TrainType,
    AdultPassenger,
    ReserveOption,
    KorailError,
)

from config import settings
from slack_client import SlackClient

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def reserve_ticket(
    client: Korail,
    dep: str,
    arr: str,
    date: str,
    start_time: str,
    start_limit: str,
    passengers: list[AdultPassenger],
):
    slack_client = SlackClient() if settings.slack_bot_token else None

    while True:
        try:
            trains = await asyncio.to_thread(
                client.search_train,
                dep=dep,
                arr=arr,
                date=date,
                time=start_time,
                train_type=TrainType.KTX,
                passengers=passengers,
            )

            # filter train with time limit
            available_trains = [
                train for train in trains if train.dep_time <= start_limit
            ]
            logger.info(f"available trains: {available_trains}")
            if len(available_trains) == 0:
                await asyncio.sleep(1)
                continue

            reservation = await asyncio.to_thread(
                client.reserve,
                train=available_trains[0],
                passengers=passengers,
                option=ReserveOption.GENERAL_ONLY,
            )
            logger.info(f"reserve success: {reservation}")
        except NoResultsError:
            logger.info("no results")
            await asyncio.sleep(1)
            continue
        except KorailError as e:
            logger.error(e)
            await asyncio.sleep(1)
            continue

        if slack_client:
            slack_client.send_message(f"reserve success: {reservation}")
        return reservation


async def main():
    korail_id = settings.korail_id
    korail_pw = settings.korail_pw

    client = Korail(korail_id, korail_pw)
    tickets_to_reserve = [
        # {
        #     "dep": "서울",
        #     "arr": "부산",
        #     "date": "20250128",
        #     "start_time": "085000",
        #     "start_limit": "093000",
        #     "passengers": [AdultPassenger(1)],
        # },
        {
            "dep": "부산",
            "arr": "서울",
            "date": "20250130",
            "start_time": "130000",
            "start_limit": "210000",
            "passengers": [AdultPassenger(1)],
        },
    ]

    tasks = [
        asyncio.create_task(reserve_ticket(client, **ticket))
        for ticket in tickets_to_reserve
    ]
    await asyncio.gather(*tasks)

    logger.info("reserve complete!")


if __name__ == "__main__":
    asyncio.run(main())

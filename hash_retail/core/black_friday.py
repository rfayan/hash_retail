import logging
from datetime import date, datetime
from os import environ


def is_black_friday() -> bool:
    black_friday = datetime.strptime(environ["BLACK_FRIDAY_DATE"], "%Y-%m-%d").date()
    today = date.today()

    day_diff = abs(black_friday - today).days
    logging.debug("Days until/past Black Friday: %s", day_diff)

    if day_diff < int(environ["BLACK_FRIDAY_INTERVAL"]):
        return True
    return False

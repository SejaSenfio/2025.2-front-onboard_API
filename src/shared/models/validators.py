from datetime import datetime as dt_datetime

from shared.validators import validate_datetime


def make_aware_if_exists(datetime: dt_datetime | None) -> dt_datetime | None:
    if datetime is None:
        return None
    return validate_datetime(datetime, make_aware=True)

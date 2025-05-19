from datetime import datetime, timezone


def get_cur_time():
    time = datetime.now(timezone.utc).strftime("[%H:%M:%S]")
    response = time + " - "
    return response

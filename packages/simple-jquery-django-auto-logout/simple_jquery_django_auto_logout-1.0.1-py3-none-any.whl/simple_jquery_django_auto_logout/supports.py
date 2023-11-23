from datetime import datetime, timedelta
from typing import Union
from django.http import HttpRequest
from django.utils.timezone import now

now = now

def seconds_until_idle_time_end(
    request: HttpRequest,
    idle_time: Union[int, timedelta],
    current_time: datetime
) -> float:
    if isinstance(idle_time, timedelta):
        ttl = idle_time
    elif isinstance(idle_time, int):
        ttl = timedelta(seconds=idle_time)
    else:
        raise TypeError(f"SIMPLE_AUTO_LOGOUT['AUTO_LOGOUT_IDLE_TIME'] `timedelta`, "
                        f"not `{type(idle_time).__name__}`.")

    if 'django_auto_logout_last_request' in request.session:
        last_req = datetime.fromisoformat(request.session['django_auto_logout_last_request'])
    else:
        last_req = current_time

    return (last_req - current_time + ttl).total_seconds()
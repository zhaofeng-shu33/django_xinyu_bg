import re
import pytz
from datetime import datetime, timedelta
# to do: use django timezone
offset_timedelta = timedelta(seconds=3600*8)
def unpack_class_name(class_name):
    re_str = '([1-9])年级([0-9]+)班'
    match_obj = re.match(re_str, class_name)
    if match_obj is None:
        raise NameError(class_name + ' not in the format ' + re_str)
    grade_id = int(match_obj.group(1))
    class_id = int(match_obj.group(2))
    return (grade_id, class_id)

def parse_time(time_string):
    # 24 小时制
    re_str = '([0-9]+)月([0-9]+)日([0-9]+):([0-9]+)-([0-9]+):([0-9]+)'
    match_obj = re.match(re_str, time_string)
    if match_obj is None:
        raise NameError(time_string + ' not in the format ' + re_str)
    month = int(match_obj.group(1))
    day = int(match_obj.group(2))
    hour_1 = int(match_obj.group(3))
    minute_1 = int(match_obj.group(4))
    hour_2 = int(match_obj.group(5))
    minute_2 = int(match_obj.group(6))    
    # to do: replace 2019 with semester info
    dt_1 = datetime(2019, month, day, hour_1, minute_1, tzinfo=pytz.UTC)
    dt_2 = datetime(2019, month, day, hour_2, minute_2, tzinfo=pytz.UTC)
    dt_3 = dt_2 - dt_1
    return (dt_1 - offset_timedelta, dt_3.seconds/60)

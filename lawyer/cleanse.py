import re

def unpack_class_name(class_name):
    re_str = '([1-9])年级([0-9]+)班'
    match_obj = re.match(re_str, class_name)
    if match_obj is None:
        raise NameError(class_name + ' not in the format ' + re_str)
    grade_id = int(match_obj.group(1))
    class_id = int(match_obj.group(2))
    return (grade_id, class_id)
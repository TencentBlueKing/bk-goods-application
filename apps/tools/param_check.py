def check_param_id(xid) -> bool:
    """
    参数id校验 - id
    """
    try:
        xid = int(xid)
        if xid > 0:
            return True
    except ValueError:
        pass
    return False


def check_param_str(p: str) -> bool:
    """
    校验参数 - str
    """
    if isinstance(p, str) and p:
        return True
    return False


def check_param_good_num(num) -> int:
    """
    校验参数 - num
    """
    if isinstance(num, int) and num > 0:
        return True
    return False


def check_param_size(size) -> int:
    try:
        if size:
            size = int(size)
            if size > 0:
                return size
    except TypeError:
        pass
    return 10


def check_param_page(page) -> int:
    try:
        if page:
            page = int(page)
            if page > 0:
                return page
    except TypeError:
        pass
    return 1


def get_error_message(serializer):
    """通过序列化器获取错误信息"""
    message = []
    errors = serializer.errors
    for key in errors:
        for detail_errors in errors[key]:
            message.append(detail_errors)
    message = ','.join(message)
    return message


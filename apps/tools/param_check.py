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


def check_apply_update_param(p: str) -> bool:
    """
    校验组内物资更新类型参数
    """
    if isinstance(p, str) and p and (p == 'status' or p == 'num'):
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
            if isinstance(detail_errors, str):
                message.append(detail_errors)
            else:
                for detail_error in errors[key][detail_errors]:
                    message.append(detail_error)
    message = ','.join(message)
    return message

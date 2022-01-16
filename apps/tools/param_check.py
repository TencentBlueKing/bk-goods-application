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



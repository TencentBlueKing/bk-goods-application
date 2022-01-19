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



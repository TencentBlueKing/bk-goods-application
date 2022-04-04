class CommonException(Exception):
    def __init__(self, enum_cls):
        self.enum_cls = enum_cls


class BusinessException(CommonException):
    """
    业务异常类
    """
    pass

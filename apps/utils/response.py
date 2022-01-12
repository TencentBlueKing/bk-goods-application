class ExceptResponse(object):
    def __init__(self, enum_cls):
        self.errmsg = enum_cls.errmsg
        self.code = enum_cls.code

    def data(self):  # 格式化数据
        return {
            'code': self.code,
            "result": False,
            "message": self.errmsg,
            "data": {}
        }
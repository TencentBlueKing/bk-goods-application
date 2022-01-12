from enum import Enum


class StatusEnums(Enum):
    """
    自定义状态
    """

    # 常见状态
    OK = (0, "成功")
    ERROR = (-1, "错误")

    # 客户端错误
    USER_ERROR = (4001, "用户名不正确")
    PWD_ERROR = (4002, "密码错误")

    # 服务端错误
    STOCK_ERROR = (5001, "库存不足")

    @property
    def code(self):
        return self.value[0]

    @property
    def errmsg(self):
        return self.value[1]
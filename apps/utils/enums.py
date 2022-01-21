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
    USER_NOTEXIST_ERROR = (4003, "缺少用户名")
    NOTFOUND_ERROR = (4004, '资源不存在')
    PARAMS_ERROR = (4005, '参数错误')
    PHONE_ERROR = (4006, '电话号码格式错误')
    NUM_ERROR = (4007, '物资数量格式错误')
    IMPORT_FILE_EMPTY_ERROR = (4008, '导入文件为空')
    AUTHORITY_ERROR = (4009, '权限不足')


    # 服务端错误
    STOCK_ERROR = (5001, "库存不足")
    CREATE_ERROR = (5002, "创建失败")
    IMPORT_ERROR = (5003, "导入失败")

    @property
    def code(self):
        return self.value[0]

    @property
    def errmsg(self):
        return self.value[1]
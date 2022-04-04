from enum import Enum


class StatusEnums(Enum):
    """
    自定义状态
    """

    # 常见状态
    OK = (0, "成功")
    ERROR = (-1, "错误")

    # 客户端错误
    USERNAME_ERROR = (4001, "用户名不正确")
    PWD_ERROR = (4002, "密码错误")
    USERNAME_NOT_EXIST_ERROR = (4003, "缺少用户名")
    # NOTFOUND_ERROR = (4004, '资源不存在')
    PARAMS_ERROR = (4005, '参数错误')
    PHONE_ERROR = (4006, '电话号码格式错误')
    NUM_ERROR = (4007, '物资数量格式错误')
    IMPORT_FILE_EMPTY_ERROR = (4008, '导入文件为空')
    AUTHORITY_ERROR = (4009, '权限不足')
    USER_NOT_EXIST_ERROR = (4010, '用户不存在，可先前往填写个人信息')
    SECRETARY_EXIST_ERROR = (4011, '用户已是管理员')
    SECRETARY_LACK_ERROR = (4012, '管理员不足')
    USER_EXIST_ERROR = (4013, '用户已存在')

    # 服务端错误
    STOCK_ERROR = (5001, "库存不足")
    CREATE_ERROR = (5002, "创建失败")
    IMPORT_ERROR = (5003, "导入失败")

    # #6XXX(申请)
    # SEARCH_ERROR = (6100, '获取相关信息失败')
    DELETE_ERROR = (6200, '处于审核状态，无法删除物资')
    NODELETE_ERROR = (6200, '物资申请不处于审核状态')
    MODIFY_ERROR = (6300, '流程被审核或终止，已无法修改')
    # AUDIT_ERROR = (6400, '管理员自身提交的申请，无需审核')
    NOAPPLY_ERROR = (6404, '物资申请不存在')
    REMARK_ERROR = (6500, '备注必须为字符串')
    #
    # #7XXX(采购)
    BLANK_ERROR = (7000, '购物车为空')
    INPUT_TYPE_ERROR = (7100, '商品类型已存在')
    CART_TYPE_ERROR = (7100, '商品类型参数不合法')
    CARTTYPE_NULL_ERROR = (7100, '商品类型不存在')
    INPUT_GOODS_ERROR = (7101, '商品名称或编号已存在')
    CART_DELETE_ERROR = (7200, '购物车物资删除失败')
    CART_ADX_ERROR = (7210, '物资删除参数错误')
    GOODID_ERROR = (7211, 'good_id参数校验出错')
    GOOD_ID_ERROR = (7211, '商品id不合法')
    CART_NULL_ERROR = (7220, '购物车中不存在该物资导致删除失败')
    CART_UPDATE_ERROR = (7220, '购物车中不存在导致数量更新失败')
    CART_UPDATE_ERROR2 = (7220, '该物资申请不存在，导致数量更新失败')
    CART_NUM_ERROR = (7230, '物资数量参数异常')
    # DELETE_PHOTOS_ERROR = (7200, '图片删除失败')
    # GOOD_OFF_THE_SHELF_ERROR = (7300, '商品已下架')
    DRAWBACK_ERROR = (7401, '商品退回原因不存在')
    SENDBACK_ERROR = (7402, '个人物资不存在，或商品不是正在使用状态')
    CART_NO_ERROR = (7404, '商品不存在')
    ADX_UPDATE_ERROR = (7500, '更新组内物资接口参数异常')
    #
    #
    # #8XXX(公共编码作为其他类)
    # USERNAME_ERROR = (8000, "用户名不正确")
    # PWD_ERROR = (8000, "密码错误")
    # AUTHORITY_ERROR = (8300, '您没有相关权限')
    NOTFOUND_ERROR = (8400, '访问资源不存在')
    # IMPORT_FILE_EMPTY_ERROR = (8410, '导入文件为空')
    AREA_ERROR = (8500, '上级地区代码参数不合法')
    APPLY_GOODS_ERROR = (8500, '物资申请列表参数不合法')
    APPLY2_GOODS_ERROR = (8500, '物资申请id不合法')
    HANDLE_ERROR = (8600, '获取失败')
    MYDELETE_ERROR = (8700, '删除失败')
    # IMPORT_FILE_FORMAT_ERROR = (8600, '文件格式错误')
    ORG_INFO_ERROR = (8800, '组信息错误')

    @property
    def code(self):
        return self.value[0]

    @property
    def errmsg(self):
        return self.value[1]

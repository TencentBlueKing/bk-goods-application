import os
import datetime

import xlwt
from django.conf import settings

from apps.good_apply.models import Apply
from apps.good_purchase.models import GroupApply, Good, GoodType, Cart


class DeriveModel(object):
    def __init__(self, model, goods, username):
        self.model = model  # 模型种类
        self.goods = goods  # 数据
        self.username = username  # 导出人
        self.work_book = xlwt.Workbook(encoding='utf-8')  # 创建excel对象
        self.work_sheet = ''
        self.excel_title = ''  # excel文件标题
        self.excel_data = []  # excel文件数据
        self.file_name = ''  # excel文件名
        self.dir_path = ''  # excel文件所在文件夹
        self.file_url = ''  # excel文件资源路径
        self.result = ''  # 标准化result

    def init_data(self):  # 初始化数据
        if self.model == 1:
            self.init_personal_data()
        elif self.model == 2:
            self.init_cart_data()
        elif self.model == 3:
            self.init_history_data()

    def init_personal_data(self):  # 初始化个人物资数据
        for group_apply_id in self.goods['selectedRows']:  # 遍历列表获得单个物资编码

            group_apply = GroupApply.objects.filter(id=group_apply_id).first()  # 根据物品编码查询对应申请表
            good_code = group_apply.good_code
            good = Good.objects.filter(good_code=good_code).first()  # 根据物品编码查询对应物品

            unit = []  # 存放一行excel信息
            unit.append(good_code)  # 物资编码

            good_name = good.good_name  # 物资名称
            unit.append(good_name)

            good_type_id = good.good_type_id  # 物资类型
            good_type = GoodType.objects.filter(id=good_type_id).first().type_name
            unit.append(good_type)

            good_price = good.price  # 物品价格
            unit.append(good_price)

            good_num = group_apply.num  # 物资数量
            unit.append(good_num)

            good_position = group_apply.position  # 所在地区
            unit.append(good_position)

            good_user = group_apply.username  # 使用人
            unit.append(good_user)

            good_user_phone = group_apply.phone  # 联系电话
            unit.append(good_user_phone)

            good_status = group_apply.get_status_display()  # 状态
            unit.append(good_status)

            self.excel_data.append(unit)  # excel列表添加一行信息

        self.work_sheet = self.work_book.add_sheet("个人物资表")
        self.excel_title = ['物资编码', '物资名称', '物品类型', '物品价格', '物品数量', '所在地区', '使用人', '使用人联系电话', '状态']  # excel标题行

    def init_cart_data(self):  # 初始化购物车数据
        for cart_id in self.goods['selectedRows']:

            unit = []  # 存放一行excel信息
            good_cart = Cart.objects.filter(id=cart_id).first()  # 根据id查询对应购物车
            good_id = good_cart.good_id
            good = Good.objects.filter(id=good_id, status=1).first()  # 根据物品id查询对应物品

            good_user = good_cart.username  # 使用人
            unit.append(good_user)

            good_code = good.good_code  # 物品编码
            unit.append(good_code)

            good_name = good.good_name  # 物品名称
            unit.append(good_name)

            good_num = good_cart.num  # 数量
            unit.append(good_num)

            good_price = good.price  # 参考单价
            unit.append(good_price)

            unit.append([])  # 需求地点
            unit.append([])  # 期望领用日期
            unit.append([])  # 标准领用日期
            unit.append([])  # 备注
            unit.append([])  # 配送方式
            unit.append([])  # 验收人
            unit.append([])  # 收货信息

            self.excel_data.append(unit)

        self.work_sheet = self.work_book.add_sheet("购物车表")
        self.excel_title = ['使用人', '物品编码', '物品名称', '数量', '参考单价', '需求地点', '期望领用日期', '标准领用日期', '备注', '配送方式', '验收人', '收货信息']  # excel标题

    def init_history_data(self):  # 初始化历史记录数据

        for apply_id in self.goods['selectedRows']:  # 遍历获取单个物品id
            unit = []  # 存放一行excel数据

            apply = Apply.objects.filter(id=apply_id).first()  # 根据申请表id查询对应申请表
            good_code = apply.good_code
            good = Good.objects.filter(good_code=good_code, status=1).first()  # 根据申请表id查询编码，再根据编码查询对应物品

            apply_user = apply.apply_user  # 使用人
            unit.append(apply_user)

            unit.append(good_code)  # 物品编码

            apply_num = apply.num  # 申请数量
            unit.append(apply_num)

            apply_position = apply.position  # 需求地点
            unit.append(apply_position)

            unit.append([])  # 期望领用日期

            apply_reason = apply.reason  # 申请原因
            unit.append(apply_reason)

            good_name = good.good_name  # 物品名称
            unit.append(good_name)

            self.excel_data.append(unit)

        work_book = xlwt.Workbook(encoding='utf-8')

        self.work_sheet = work_book.add_sheet("物资申请历史记录表")
        self.excel_title = ['使用人', '物品编码', '申请数量', '需求地点', '期望领用日期', '备注', '物品名称']  # excel标题

    def init_excel(self):  # 初始化excel表格
        style = xlwt.XFStyle()
        font = xlwt.Font()
        # 加粗标题字体
        font.bold = True
        style.font = font

        # 写入标题
        for index, item in enumerate(self.excel_title):
            self.work_sheet.write(0, index, item, style)

        # 写入数据
        for index_row, item in enumerate(self.excel_data):
            for index_col, unit in enumerate(item):
                self.work_sheet.write(index_row + 1, index_col, unit)

        # 设置宽度
        for index, item in enumerate(self.excel_title):
            self.work_sheet.col(index).width = 3800

    def save_excel(self):
        # 保存
        # 规定文件名
        if self.model == 1:
            self.file_name = self.username + '_personal_goods_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'
        elif self.model == 2:
            self.file_name = self.username + '_cart_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'
        elif self.model == 3:
            self.file_name = self.username + '_apply_history_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'
        # 规定文件夹名
        if self.model == 1:
            self.dir_path = os.path.join(settings.MEDIA_ROOT, 'personal_goods')
        elif self.model == 2:
            self.dir_path = os.path.join(settings.MEDIA_ROOT, 'cart')
        elif self.model == 3:
            self.dir_path = os.path.join(settings.MEDIA_ROOT, 'apply_history')

        # 检查文件夹是否存在
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        # 拼接文件路径
        file_path = os.path.join(self.dir_path, self.file_name)

        self.work_book.save(file_path)

    def derive_result(self):
        if self.model == 1:
            self.file_url = settings.BK_BACK_URL + '/media/' + 'personal_goods/' + self.file_name
        elif self.model == 2:
            self.file_url = settings.BK_BACK_URL + '/media/' + 'cart/' + self.file_name
        elif self.model == 3:
            self.file_url = settings.BK_BACK_URL + '/media/' + 'apply_history/' + self.file_name

        self.result = {
            "code": 200,
            "result": True,
            "message": "OK",
            "data": {
                'file_url': self.file_url  # 返回资源地址
            }
        }

    def run(self):
        self.init_data()
        self.init_excel()
        self.save_excel()
        self.derive_result()

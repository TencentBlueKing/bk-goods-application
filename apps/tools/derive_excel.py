import datetime
import json
import os

from django.views.decorators.http import require_POST
import xlwt

from apps.good_apply.models import Apply
from apps.good_purchase.models import Good, Cart, GoodType, GroupApply
from apps.tools.response import get_result
from django.conf import settings
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException


@require_POST
def derive_excel(request):
    """
    导出excel表
    """
    body = request.body
    body = json.loads(body)
    if body['model']:
        model = body['model']
    if body['dataList']:
        goods = body['dataList']

    if not model or not goods:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    if model == 1:  # 个人物资查询导出模式
        excel_data = []
        try:
            for good_code in goods['selectedRows']:  # 遍历列表获得单个物资编码
                unit = []  # 存放一行excel信息
                unit.append(good_code)  # 物资编码

                good = Good.objects.filter(good_code=good_code).first()  # 根据物品编码查询对应物品
                group_apply = GroupApply.objects.filter(good_code=good_code).first()  # 根据物品编码查询对应申请表

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

                excel_data.append(unit)  # excel列表添加一行信息

            work_book = xlwt.Workbook(encoding='utf-8')  # 创建excel对象
            work_sheet = work_book.add_sheet("个人物资表")

            excel_title = ['物资编码', '物资名称', '物品类型', '物品价格', '物品数量', '所在地区', '使用人', '使用人联系电话', '状态']  # excel标题行
            style = xlwt.XFStyle()
            font = xlwt.Font()
            # 加粗标题字体
            font.bold = True
            style.font = font
            for index, item in enumerate(excel_title):  # 写入标题
                work_sheet.write(0, index, item, style)

            # 写入数据
            for index_row, item in enumerate(excel_data):
                for index_col, unit in enumerate(item):
                    work_sheet.write(index_row + 1, index_col, unit)

            # 设置宽度
            for index, item in enumerate(excel_title):
                work_sheet.col(index).width = 3800

            # 保存
            # 规定文件名
            file_name = good_user + '_personal_goods_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'

            # 规定文件夹名
            dir_path = os.path.join('USERRES', 'personal_goods')

            # 检查文件夹是否存在
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # 拼接文件路径
            file_path = os.path.join(dir_path, file_name)

            work_book.save(file_path)

            result = {
                "code": 200,
                "result": True,
                "message": "OK",
                "data": {
                    'file_url': settings.BK_BACK_URL + '/media/' + 'personal_goods/' + file_name  # 返回资源路径
                }
            }
            return get_result(result)
        except Exception as e:
            raise ValueError(e)
    elif model == 2:  # 购物车导出模式
        excel_data = []  # 存放excel信息
        try:
            for good_id in goods['selectedRows']:
                unit = []  # 存放一行excel信息

                good = Good.objects.filter(id=good_id).first()  # 根据物品id查询对应物品
                good_cart = Cart.objects.filter(good_id=good_id).first()  # 根据物品id查询对应购物车

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

                excel_data.append(unit)

            work_book = xlwt.Workbook(encoding='utf-8')
            work_sheet = work_book.add_sheet("购物车表")

            excel_title = ['使用人', '物品编码', '物品名称', '数量', '参考单价', '需求地点', '期望领用日期', '标准领用日期', '备注', '配送方式', '验收人', '收货信息']  # excel标题
            style = xlwt.XFStyle()
            font = xlwt.Font()
            # 加粗标题字体
            font.bold = True
            style.font = font

            # 写入标题
            for index, item in enumerate(excel_title):
                work_sheet.write(0, index, item, style)

            # 写入数据
            for index_row, item in enumerate(excel_data):
                for index_col, unit in enumerate(item):
                    work_sheet.write(index_row + 1, index_col, unit)

            # 设置宽度
            for index, item in enumerate(excel_title):
                work_sheet.col(index).width = 3800

            # 保存
            # 规定文件名
            file_name = good_user + '_cart_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'

            # 规定文件夹名
            dir_path = os.path.join('USERRES', 'cart')

            # 检查文件夹是否存在
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # 拼接文件路径
            file_path = os.path.join(dir_path, file_name)
            work_book.save(file_path)

            result = {
                "code": 200,
                "result": True,
                "message": "OK",
                "data": {
                    'file_url': settings.BK_BACK_URL + '/media/' + 'cart/' + file_name  # 返回资源地址
                }
            }
            return get_result(result)
        except Exception as e:
            raise ValueError(e)

    elif model == 3:  # 历史记录导出模式
        excel_data = []
        try:
            for apply_id in goods['selectedRows']:  # 遍历获取单个物品id
                unit = []  # 存放一行excel数据

                apply = Apply.objects.filter(id=apply_id).first()  # 根据申请表id查询对应申请表
                good_code = apply.good_code
                good = Good.objects.filter(good_code=good_code).first()  # 根据申请表id查询编码，再根据编码查询对应物品

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

                excel_data.append(unit)

            work_book = xlwt.Workbook(encoding='utf-8')
            work_sheet = work_book.add_sheet("物资申请历史记录表")

            excel_title = ['使用人', '物品编码', '申请数量', '需求地点', '期望领用日期', '备注', '物品名称']  # excel标题
            style = xlwt.XFStyle()
            font = xlwt.Font()
            # 加粗标题字体
            font.bold = True
            style.font = font

            # 写入标题
            for index, item in enumerate(excel_title):
                work_sheet.write(0, index, item, style)

            # 写入数据
            for index_row, item in enumerate(excel_data):
                for index_col, unit in enumerate(item):
                    work_sheet.write(index_row + 1, index_col, unit)

            # 设置宽度
            for index, item in enumerate(excel_title):
                work_sheet.col(index).width = 3800

            # 保存
            # 规定文件名
            file_name = apply_user + '_apply_history_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'

            # 规定文件夹名
            dir_path = os.path.join('USERRES', 'apply_history')

            # 检查文件夹是否存在
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # 拼接路径
            file_path = os.path.join(dir_path, file_name)
            work_book.save(file_path)

            result = {
                "code": 200,
                "result": True,
                "message": "OK",
                "data": {
                    'file_url': settings.BK_BACK_URL + '/media/' + 'apply_history/' + file_name  # 返回资源地址
                }
            }
            return get_result(result)
        except Exception as e:
            raise ValueError(e)

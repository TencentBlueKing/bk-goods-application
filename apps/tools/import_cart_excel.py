import base64
import os.path

import xlrd
from apps.good_purchase.models import Good, GroupApply, UserInfo
# from apps.good_purchase.serializers import GroupApplySerializers
from apps.tools.generate_can_not_add_excel import generate_can_not_add_excel
from apps.tools.response import get_result
from apps.tools.tool_get_import_file import tool_get_import_file
from apps.tools.tool_get_xls_excel_data import tool_get_xls_excel_data
from apps.tools.tool_get_xlsx_excel_data import tool_get_xlsx_excel_data
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.views.decorators.http import require_POST
from openpyxl import load_workbook


@require_POST
def import_cart_excel(request):
    def handle_excel_data(rows, CANNOT_ADD, err_msg):  # 处理传入的列表数据，判断是否加入部门所需物资表
        group_apply_create_list = []  # 存放GroupApply对象
        for row_index, row in enumerate(rows):
            if row_index == 0:  # 标题行
                title = ['使用人', '物品编码', '数量', '需求地点', '期望领用日期', '备注', '物品名称']
                if row != title:
                    return ['文件格式错误']
                continue

            gapply_item = row

            username = gapply_item[0]
            good_code = gapply_item[1]

            # 判断商品是否存在于商品表中，判断用户名是否存在于用户表中
            if not Good.objects.filter(good_code=good_code, status=1).exists():
                CANNOT_ADD.append(good_code)
                err_msg.append('{}: 无对应商品'.format(good_code))
                continue
            if not UserInfo.objects.filter(username=username).exists():
                CANNOT_ADD.append(good_code)
                err_msg.append('{}: 无对应用户'.format(good_code))
                continue

            phone = ''
            if UserInfo.objects.filter(username=username).first().phone:
                phone = UserInfo.objects.filter(username=username).first().phone

            num = gapply_item[2]

            # 判断数量是否为整形或浮点型，并且是否大于等于0
            if (not isinstance(num, int) and not isinstance(num, float)) or not num >= 0:
                CANNOT_ADD.append(good_code)
                err_msg.append('{}: 数量格式有误'.format(good_code))
                continue

            position = gapply_item[3]

            # get_date = gapply_item[4]
            remarks = gapply_item[5]
            # good_name = gapply_item[6]
            group_apply_create_list.append(GroupApply(good_code=good_code, num=num, username=username, position=position
                                                      , phone=phone, status=4, remarks=remarks))

        # 若无问题数据
        if not CANNOT_ADD:
            GroupApply.objects.bulk_create(group_apply_create_list)

    body = request.body
    username = request.user.username

    dir_path = 'import_cart_excel'
    file, file_path = tool_get_import_file(body, dir_path, 'file', 'fileName')

    # 将file以base64格式译码
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(file))

    # 获取文件类型，支持xlsx于xls
    file_type = file_path.split('/')[-1].split('.')[-1]

    # 存放问题数据
    CANNOT_ADD = []
    err_msg = []
    if file_type == 'xlsx':
        xlsx = load_workbook(file_path)
        table = xlsx.worksheets[0]

        # 取得excel文件数据
        rows = tool_get_xlsx_excel_data(table)

        # 删除项目本地文件
        if os.path.exists(file_path):
            os.remove(file_path)

        if len(rows) > 1:
            receive_handle_result = handle_excel_data(rows, CANNOT_ADD, err_msg)  # 处理数据
        else:
            raise BusinessException(StatusEnums.IMPORT_FILE_EMPTY_ERROR)

    elif file_type == 'xls':
        xls = xlrd.open_workbook(file_path)
        table = xls.sheets()[0]

        # 取得excel文件数据
        # for row_idx in range(table.nrows):
        #     rows.append(table.row_values(row_idx))
        rows = tool_get_xls_excel_data(table)

        # 删除项目本地文件
        if os.path.exists(file_path):
            os.remove(file_path)

        if len(rows) > 1:
            receive_handle_result = handle_excel_data(rows, CANNOT_ADD, err_msg)  # 处理数据
        else:
            raise BusinessException(StatusEnums.IMPORT_FILE_EMPTY_ERROR)

    if receive_handle_result == ['文件格式错误']:
        result = {
            "code": 400,
            "result": False,
            "message": receive_handle_result,
            "data": {}
        }
        return get_result(result)

    if not CANNOT_ADD:
        result = {
            "code": 200,
            "result": True,
            "message": "导入成功",
            "data": {}
        }
        return get_result(result)
    else:
        can_not_add_file_url = generate_can_not_add_excel(CANNOT_ADD, username, err_msg)
        result = {
            "code": StatusEnums.IMPORT_ERROR.code,
            "result": True,
            "message": "部分/全部excel数据" + StatusEnums.IMPORT_ERROR.errmsg,
            "data": {
                'created_fail_list': CANNOT_ADD,
                'file_url': can_not_add_file_url
            }
        }
        return get_result(result)

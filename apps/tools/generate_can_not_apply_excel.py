import datetime
import os

import xlwt
from blueapps.conf import settings


def generate_can_not_apply_excel(can_not_apply_list, username):
    work_book = xlwt.Workbook(encoding='utf-8')  # 创建excel对象
    work_sheet = work_book.add_sheet('格式错误物资表')
    excel_title = ['使用人', '物品编码', '物品名称', '数量', '参考单价', '需求地点',
                   '期望领用日期', '标准领用日期', '备注', '配送方式', '验收人', '收货信息']  # excel标题
    style = xlwt.XFStyle()
    font = xlwt.Font()
    # 加粗标题字体
    font.bold = True
    style.font = font

    # 写入标题
    for index, item in enumerate(excel_title):
        work_sheet.write(0, index, item, style)

    # 写入数据
    for index_row, row in enumerate(can_not_apply_list):
        for index_col, col in enumerate(row):
            work_sheet.write(index_row + 1, index_col, col)

    # 设置宽度
    for index, item in enumerate(excel_title):
        work_sheet.col(index).width = 3800

    file_name = username + '_analysis_err_code_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'

    dir_path = os.path.join(settings.MEDIA_ROOT, 'analysis_err_excel')

    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 拼接文件路径
    file_path = os.path.join(dir_path, file_name)

    work_book.save(file_path)

    file_url = settings.BK_BACK_URL + '/media/' + 'analysis_err_excel/' + file_name

    return file_url

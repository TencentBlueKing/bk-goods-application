import datetime
import os

import xlwt
from bkstorages.backends.bkrepo import BKRepoStorage


def generate_can_not_add_excel(err_code_list, username, err_msg, org_name):
    """
    生成添加失败excel
    err_code_list: 有错误的物品编码列表
    username: 用户名
    err_msg: 错误信息
    """
    work_book = xlwt.Workbook(encoding='utf-8')  # 创建excel对象
    work_sheet = work_book.add_sheet('格式错误物资表')
    excel_title = ['错误物资编码']

    style = xlwt.XFStyle()
    font = xlwt.Font()
    # 加粗标题字体
    font.bold = True
    style.font = font

    # 写入标题
    for index, item in enumerate(excel_title):
        work_sheet.write(0, index, item, style)

    # 写入数据
    for index, item in enumerate(err_code_list):
        work_sheet.write(index + 1, 0, item)
    # 写入标题
    work_sheet.write(len(err_code_list) + 1, 0, '错误信息', style)

    # 写入错误信息
    for index, item in enumerate(err_msg):
        work_sheet.write(index + 1 + 1 + len(err_code_list), 0, item)

    # 设置宽度
    for index, item in enumerate(excel_title):
        work_sheet.col(index).width = 3800

    file_name = username + '_import_err_code_' + datetime.datetime.today().strftime('%Y-%m-%d__%H') + '.xls'

    dir_path = os.path.join(org_name, 'import_err_excel')

    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 拼接文件路径
    file_path = os.path.join(dir_path, file_name)

    work_book.save(file_path)

    storage = BKRepoStorage()
    with open(file_path, 'rb') as f:
        storage.save(file_path, f)

    # 删除项目本地文件
    if os.path.exists(file_path):
        os.remove(file_path)

    # file_url = settings.BK_BACK_URL + '/media/' + 'import_err_excel/' + file_name
    file_url = storage.url(file_path)

    return file_url

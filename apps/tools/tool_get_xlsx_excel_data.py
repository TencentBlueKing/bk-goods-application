from blueapps import account


def tool_get_xlsx_excel_data(table):
    # 获取xlsx文件数据
    """
    table: xlsx工作表
    """
    rows = []
    for i in range(1, table.max_row + 1):
        row = [table.cell(i, index).value for index in range(1, table.max_column + 1)]
        rows.append(row)
    return rows


account.get_user_model()

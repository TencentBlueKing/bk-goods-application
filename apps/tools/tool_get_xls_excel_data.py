def tool_get_xls_excel_data(table):
    # 获取xls文件数据
    """
    table: xls工作表
    """
    rows = []
    for row_idx in range(table.nrows):
        rows.append(table.row_values(row_idx))
    return rows

import datetime


def tool_get_start_end(req_data, params_start_time, params_end_time):
    # 开始，结束时间处理
    """
    req_data: 请求的数据
    params_start_time: 前端传入开始时间参数名
    params_end_time: 前端传入结束时间参数名
    """
    start_time = req_data.get(params_start_time, None)
    end_time = req_data.get(params_end_time, None)

    if start_time and end_time:
        if not start_time <= end_time:
            raise ValueError('开始日期不能大于结束日期')

    if not start_time:
        start_time = '1970-1-1'
    if not end_time:
        end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        end_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d")
                    + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    return start_time, end_time

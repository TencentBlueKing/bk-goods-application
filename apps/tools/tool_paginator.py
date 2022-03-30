from apps.tools.param_check import check_param_page, check_param_size
from django.core.paginator import Paginator


def tool_paginator(req_data, model, query, params_page, params_size):
    # 页码处理
    """
    req_data: 请求中所携带的数据
    model: 需要查询的model
    query: 筛选条件（Q类型）
    params_page: 前端传入的页数参数名
    params_size: 前端传入的页面数据量的参数名
    """
    page = req_data.get(params_page, 1)
    page = check_param_page(page)
    size = req_data.get(params_size, 10)
    size = check_param_size(size)

    queryset = model.objects.filter(query).order_by("-update_time")
    total_num = queryset.count()
    paginator = Paginator(queryset, size)
    paged_queryset = paginator.get_page(page)

    return paged_queryset, total_num

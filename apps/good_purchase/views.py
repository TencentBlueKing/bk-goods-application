# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import collections

from django.core.paginator import Paginator
from django.db.models import Q

from apps.good_purchase.models import Good, GoodType
from apps.tools.param_check import check_param_id
from apps.tools.response import get_result
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from django.views.decorators.http import require_GET

from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException


@require_GET
def get_good_detail(request):
    """
    根据商品id获取商品详情信息
    """
    good_id = request.GET.get("good_id", 0)
    # 校验参数
    if not check_param_id(good_id):
        return get_result({"code": 1, "result": False, "message": "good_id参数校验出错"})
    try:
        good = Good.objects.get(id=good_id, status=1).to_json()
    except Good.DoesNotExist:
        return get_result({"code": 1, "result": False, "message": "商品不存在"})
    return get_result({"data": good})


def get_goods(request):

    if request.method == "GET":
        good_name = request.GET.get('name', None)
        good_type = request.GET.get('type', None)
        page = request.GET.get('page', 1)
        if not page.isdigit():  # 若页数为非数字
            page = 1

        if good_type == "0":  # good_type为0指的是所有类型
            good_type = None

        query = Q(status=1)
        if good_name:  # 若存在搜索内容
            query = query & Q(good_name__icontains=good_name)
        if good_type:  # 若指定了商品类型
            query = query & Q(good_type_id=good_type)
        queryset = Good.objects.filter(query)  # 获得指定的查询集
        paginator = Paginator(queryset, 8)  # 获取分页器对象
        queryset = paginator.get_page(page)  # 获取指定页数内容，若无指定默认为第一页
        serializer_data = []
        for item in queryset:
            serializer_data.append(item.to_json())
        pageNum_dict = collections.OrderedDict()  # 创建OrderedDict对象
        pageNum_dict['page_count'] = queryset.paginator.num_pages  # 将page_count加入到OrderedDict对象
        serializer_data.append(pageNum_dict)  # 将新建的OrderedDict与序列化后的数据拼接
        data = {
            "code": 200,
            "result": True,
            "message": "OK",
            "data": serializer_data
        }
        return get_result(data)

    else:
        data = {
            "code": 405,
            "result": True,
            "message": "OK",
            "data": '请求方法只能为get'
        }
        return get_result(data)


def get_types(request):
    """
    获取所有类型
    """
    if request.method == "GET":  # 指定请求方法
        queryset = GoodType.objects.all()
        serializer_data = []
        for item in queryset:
            serializer_data.append(item.to_json())
        data = {
            "code": 200,
            "result": True,
            "message": "OK",
            "data": serializer_data
        }
        return get_result(data)

    else:
        data = {
            "code": 405,
            "result": True,
            "message": "OK",
            "data": '请求方法只能为get'
        }
        return get_result(data)

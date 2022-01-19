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
import json
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from apps.good_purchase.models import Good, GoodType, Cart, UserInfo, GroupApply
from apps.tools.param_check import check_param_id, check_param_str, check_apply_update_param
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


def get_shopping_cart(request):
    """
    获取购物车信息
    """
    username = request.GET.get("userName")
    if not check_param_str(username):
        return get_result({"code": 4005, "result": False, "message": "参数不合法"})
    if not UserInfo.objects.filter(username=username).exists():
        return get_result({"code": 4004, "result": False, "message": "用户不存在"})
    good_list = Cart.objects.filter(username=username)
    cart_list = []
    for good in good_list:
        good = good.to_json()
        if good["status"] == 1:
            has_type = False
            for type_item in cart_list:
                if type_item["goods_type_name"] == good["good_type_name"]:
                    type_item["goods_list"].append(good)
                    has_type = True
                    break
            if not has_type:
                temp_obj = {
                    "goods_type_name": good["good_type_name"],
                    "goods_type_id": good["good_type_id"],
                    "goods_list": [good]
                }
                cart_list.append(temp_obj)
    if len(cart_list) == 0:
        return get_result({"code": 200, "data": [], "message": "购物车为空"})
    return get_result({"code": 200, "data": cart_list})


def delete_cart_goods(request):
    """
    删除购物车中物资
    """
    req = json.loads(request.body)
    goods_id_list = req.get("goodsIdList")
    if not isinstance(goods_id_list, list):
        return get_result({"code": 4005, "result": False, "message": "物资删除参数错误"})
    try:
        Cart.objects.filter(id__in=goods_id_list).delete()
    except Cart.DoesNotExist:
        return get_result({"code": 4004, "result": False, "message": "删除失败"})
    return get_result({"code": 200, "message": "删除成功"})


def add_cart_goods(request):
    """
    物资加入购物车物
    """
    req = json.loads(request.body)
    good_info = req.get("goodInfo")
    temp_good = Cart.objects.filter(id=good_info["id"])
    if temp_good.exists():
        num = int(temp_good[0].num) + int(good_info["num"])
        Cart.objects.filter(id=good_info["id"]).update(num=num, update_time=datetime.now())
    else:
        Cart.objects.create(good_id=good_info['id'], username=good_info['username'], num=good_info['num'])
    return get_result({"code": 200, "message": "修改成功"})


def update_cart_goods(request):
    """
    更新购物车物资数量信息
    """
    req = json.loads(request.body)
    update_goods_list = req.get("goodsList")
    if isinstance(update_goods_list, list):
        all_goods = []
        for good in update_goods_list:
            try:
                temp_good = Cart.objects.get(id=good["id"])
            except Cart.DoesNotExist:
                return get_result({"code": 4004, "result": False, "message": "该物资不存在，导致数量更新失败。"})
            temp_good.num = int(good["num"])
            temp_good.update_time = datetime.now()
            all_goods.append(temp_good)
        Cart.objects.bulk_update(all_goods, ['num', 'update_time'])
    else:
        return get_result({"code": 4005, "result": False, "message": "物资数量参数异常"})
    return get_result({"code": 200, "message": "修改成功"})


def get_group_apply(request):
    """
    获取组内物资信息
    """
    apply_list = GroupApply.objects.filter(status=4)
    cart_list = []
    if apply_list.exists():
        for apply in apply_list:
            apply = apply.to_good_json(apply.good_code)
            has_type = False
            for type_item in cart_list:
                if type_item["goods_type_name"] == apply["good_type_name"]:
                    type_item["goods_list"].append(apply)
                    has_type = True
                    break
            if not has_type:
                temp_obj = {
                    "goods_type_name": apply["good_type_name"],
                    "goods_type_id": apply["good_type_id"],
                    "goods_list": [apply]
                }
                cart_list.append(temp_obj)
    return get_result({"code": 200, "data": cart_list, "message": "获取成功"})


def delete_group_apply(request):
    """
    删除组内物资
    """
    req = json.loads(request.body)
    apply_id = req.get("applyId")
    if not check_param_id(apply_id):
        return get_result({"code": 4005, "result": False, "message": "组内物资删除参数错误"})
    try:
        GroupApply.objects.get(id=apply_id).delete()
    except GroupApply.DoesNotExist:
        return get_result({"code": 501, "result": False, "message": "组内物资删除失败"})
    return get_result({"code": 200, "message": "删除成功"})


def update_group_apply(request):
    """
    更新申请物资数量信息
    """
    req = json.loads(request.body)
    apply_list = req.get("applyList")
    update_type = req.get("updateType")
    if isinstance(apply_list, list) and check_apply_update_param(update_type):
        all_applies = []
        for apply in apply_list:
            try:
                temp_apply = GroupApply.objects.get(id=apply["id"])
            except GroupApply.DoesNotExist:
                return get_result({"code": 4004, "result": False, "message": "该物资不存在，导致更新失败。"})
            temp_apply.num = int(apply["num"])
            if update_type == 'status':
                temp_apply.status = 2
            temp_apply.update_time = datetime.now()
            all_applies.append(temp_apply)
        if update_type == 'status':
            GroupApply.objects.bulk_update(all_applies, ['status', 'update_time'])
        else:
            GroupApply.objects.bulk_update(all_applies, ['num', 'update_time'])
    else:
        return get_result({"code": 4005, "result": False, "message": "更新组内物资接口参数异常"})
    return get_result({"code": 200, "message": "修改成功"})


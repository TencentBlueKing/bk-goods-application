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
import base64
import collections
import json
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from apps.good_purchase.models import Good, GoodType, Cart, UserInfo, GroupApply
from apps.tools.param_check import check_param_id, check_param_str, check_apply_update_param

import uuid
from apps.good_purchase.serializers import GoodSerializers, GoodTypeSerializers
from apps.tools.param_check import (check_param_id, check_param_page,
                                    check_param_size, check_param_str,
                                    get_error_message)
from apps.tools.response import get_result, get_cart_result, get_apply_result
from config.default import os
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from django.views.decorators.http import require_GET, require_POST


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
    cart_list = get_cart_result(good_list)
    if len(cart_list) == 0:
        return get_result({"code": 200, "data": [], "message": "购物车为空"})
    return get_result({"code": 200, "data": cart_list})


def delete_cart_goods(request):
    """
    删除购物车中物资
    """
    req = json.loads(request.body)
    username = req.get("userName")
    cart_id_list = req.get("cartIdList")
    if not isinstance(cart_id_list, list):
        cart_all_id = Cart.objects.filter(username=username).values_list("id", flat=True)
        if not set(cart_id_list).issubset(set(cart_all_id)):
            return get_result({"code": 4005, "result": False, "message": "物资删除参数错误"})
    if not Cart.objects.filter(id__in=cart_id_list, username=username).exists():
        return get_result({"code": 4004, "result": False, "message": "购物车中不存在该物资导致删除失败"})
    Cart.objects.filter(id__in=cart_id_list).delete()
    return get_result({"code": 200, "message": "删除成功"})


def add_cart_goods(request):
    """
    物资加入购物车物
    """
    req = json.loads(request.body)
    good_info = req.get("goodInfo")
    if isinstance(good_info['num'], int) and good_info['num'] > 0:
        if not UserInfo.objects.filter(username=good_info["username"]).exists():
            return get_result({"code": 4005, "result": False, "message": "用户名参数验证失败"})
        temp_good = Cart.objects.filter(good_id=good_info["id"], username=good_info["username"])
    else:
        return get_result({"code": 4005, "result": False, "message": "物资数量参数错误"})
    if temp_good.exists():
        num = int(temp_good[0].num) + int(good_info["num"])
        Cart.objects.filter(good_id=good_info["id"]).update(num=num, update_time=datetime.now())
    else:
        Cart.objects.create(good_id=good_info['id'], username=good_info['username'], num=good_info['num'])
    return get_result({"code": 200, "message": "物资成功加入购物车"})


def update_cart_goods(request):
    """
    更新购物车物资数量信息
    """
    req = json.loads(request.body)
    update_goods_list = req.get("goodsList")
    if isinstance(update_goods_list, list):
        update_goods_ids = []
        for update_goods in update_goods_list:
            update_goods_ids.append(update_goods["id"])
        cart_all_id = Cart.objects.values_list("id", flat=True)
        if not set(update_goods_ids).issubset(set(cart_all_id)):
            return get_result({"code": 4004, "result": False, "message": "物资不存在，导致数量更新失败。"})
        all_goods = []
        for good in update_goods_list:
            temp_good = Cart.objects.get(id=good["id"])
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
    if not apply_list.exists():
        return get_result({"code": 200, "data": [], "message": "申请状态为购买中的列表为空"})
    cart_list = get_apply_result(apply_list)
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
        return get_result({"code": 4004, "result": False, "message": "组内物资删除失败"})
    return get_result({"code": 200, "message": "删除成功"})


def update_group_apply(request):
    """
    更新申请物资数量信息
    """
    req = json.loads(request.body)
    apply_list = req.get("applyList")
    update_type = req.get("updateType")
    if isinstance(apply_list, list) and check_apply_update_param(update_type):
        update_apply_ids = []
        for update_apply in update_apply_ids:
            update_apply_ids.append(update_apply["id"])
        all_apply_id = GroupApply.objects.values_list("id", flat=True)
        if not set(update_apply_ids).issubset(set(all_apply_id)):
            return get_result({"code": 4004, "result": False, "message": "该物资申请不存在，导致数量更新失败。"})
        all_applies = []
        for apply in apply_list:
            temp_apply = GroupApply.objects.get(id=apply["id"])
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


@require_GET
def get_good_list(request):
    """
    获取商品列表
    """
    # 筛选项参数拼接查询条件
    query = Q(status=1)
    # 需要筛选的字段
    conditions = ('good_code', 'good_name')
    for condition in conditions:
        # 查询筛选值
        condition_value = request.GET.get(condition, None)
        if check_param_str(condition_value):
            # 新建模糊查询筛选条件字典
            new_query = {condition + '__contains': condition_value}
            # 拼接筛选条件
            query = query & Q(**new_query)

    # 商品类型筛选条件
    good_type_id = request.GET.get("good_type_id", 0)
    try:
        good_type_id = int(good_type_id)
        if good_type_id > 0:
            query = query & Q(good_type_id=good_type_id)
    except ValueError:
        get_result({"code": 1, "result": False, "message": "商品类型参数不合法"})
    # 分页
    page = request.GET.get('page', 1)
    page = check_param_page(page)
    size = request.GET.get('size', 10)
    size = check_param_size(size)
    # 查询
    goods = Good.objects.filter(query).order_by("-update_time")
    # 生成分页器对象，指定每一页有多少个条元素
    paginator = Paginator(goods, size)
    cur_goods = paginator.get_page(page)  # 获取指定页元素，获取当前页的商品 ！要不要try catch
    # 返回数据
    data = {"total_num": goods.count(),
            "good_list": [good.to_json() for good in cur_goods]}  # ！这里还是for循环内部查询了数据库
    return get_result({"data": data})


@require_GET
def get_good_type_list(request):
    """获取商品类别列表"""
    good_types = GoodType.objects.all()
    good_type_list = [good_type.to_json() for good_type in good_types]
    return get_result({"data": good_type_list})


@require_POST
def add_good(request):
    """添加商品"""
    good = json.loads(request.body)
    # 参数校验
    good_serializers = GoodSerializers(data=good)
    if not good_serializers.is_valid():
        message = get_error_message(good_serializers)
        return get_result({"code": 1, "result": False, "message": message})  # 输出错误方式
    # 检查商品编码是否存在
    if Good.objects.filter(good_code=good.get("good_code")).exists():
        return get_result({"code": 1, "result": False, "message": "商品编码已存在"})
    # 检验商品类型是否存在
    type_id = good.get("good_type_id")
    try:
        GoodType.objects.get(id=type_id)
    except GoodType.DoesNotExist:
        return get_result({"code": 1, "result": False, "message": "商品类型不存在"})
    with transaction.atomic():
        Good.objects.create(**good)
    return get_result({"message": "新增商品成功"})


def update_good(request):
    """修改商品信息"""
    good = json.loads(request.body)
    # 参数校验
    good_serializers = GoodSerializers(data=good)
    if not good_serializers.is_valid():
        message = get_error_message(good_serializers)
        return get_result({"code": 1, "result": False, "message": message})
    try:
        # 校验id
        good_id = good.get("id", 0)
        if not check_param_id(good_id):
            return get_result({"code": 1, "result": False, "message": "商品id不合法"})
        # 检验编码是否重复(good_code相同，但id不同的商品)
        goods = Good.objects.filter(Q(good_code=good.get("good_code")) & ~Q(id=good_id))
        if goods:
            return get_result({"code": 1, "result": False, "message": "商品编号已存在"})
        # 校验商品类型是否存在
        type_id = good.get("good_type_id")
        GoodType.objects.get(id=type_id)
        # 校验商品是否存在
        Good.objects.get(id=good_id)
        # 更新数据
        Good.objects.filter(id=good_id).update(**good)
    except Good.DoesNotExist:
        return get_result({"code": 1, "result": False, "message": "商品不存在"})
    except GoodType.DoesNotExist:
        return get_result({"code": 1, "result": False, "message": "商品类型不存在"})
    return get_result({"message": "修改商品信息成功"})


@require_POST
def down_good(request):
    """商品下架"""
    good_id = json.loads(request.body).get('good_id')
    # 校验参数
    if not check_param_id(good_id):
        return get_result({"code": 1, "result": False, "message": "good_id参数校验出错"})
    # 是否存在商品不存在的情况
    Good.objects.filter(id=good_id).update(status=0)
    return get_result({"message": "下架商品成功"})


@require_POST
def add_good_type(request):
    """新增商品类型"""
    good_type = json.loads(request.body)
    # 参数校验
    good_type_serializers = GoodTypeSerializers(data=good_type)
    if not good_type_serializers.is_valid():
        message = get_error_message(good_type_serializers)
        return get_result({"code": 1, "result": False, "message": message})
    # 验证该商品类型是否存在
    type_name = good_type.get("type_name")
    good_types = GoodType.objects.filter(type_name=type_name)
    if good_types:
        return get_result({"code": 1, "result": False, "message": "商品类型名称已存在"})
    good_type = GoodType.objects.create(type_name=type_name)
    return get_result({"message": "新增商品类型成功", "data": {"id": good_type.id}})


@require_POST
def upload_img(request):
    """上传图片"""
    req = json.loads(request.body)
    img_obj = req.get("img")
    file_type = req.get("img_type")
    # 生成随机数命名图片
    file_name = str(uuid.uuid4()) + '.' + file_type
    # 判断文件夹是否存在
    dir_path = os.path.join(settings.MEDIA_ROOT, 'good_purchase')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_path = os.path.join(dir_path, file_name)
    # 写入图片
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(img_obj))
    pic_url = settings.BK_BACK_URL + '/media/good_purchase/' + file_name
    return get_result({"message": "上传图片成功", "data": {"pic_url": pic_url}})

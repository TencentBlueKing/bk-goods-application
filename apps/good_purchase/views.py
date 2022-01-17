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
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST

from apps.good_purchase.models import Good, GoodType, GroupApply, Cart
from apps.good_purchase.serializers import GoodSerializers, GoodTypeSerializers
from apps.tools.param_check import (check_param_id, check_param_page,
                                    check_param_size, check_param_str,
                                    get_error_message)
from apps.tools.response import get_result
from config.default import os
from django.conf import settings
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

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


@require_GET
def get_personal_goods(request):
    """
    获取个人物资
    """
    # 获取params
    username = request.GET.get('username', None)
    form = request.GET.get('form', None)
    page_limit = int(request.GET.get('pageLimit', 10))
    page = int(request.GET.get('page', 1))

    # 若params没有username则报错
    if not username:
        raise BusinessException(StatusEnums.USER_NOTEXIST_ERROR)

    # 获得查询集
    queryset = GroupApply.objects.filter(username=username)

    unnecessary_goods = []  # 用于记录被过滤掉的物品

    # 若form存在
    if form:
        # 获取form的内容
        form = json.loads(form)
        name = form['name'] if form['name'] else None
        code = form['code'] if form['code'] else None
        location = form['location'] if form['location'] else None
        status = int(form['status']) if form['status'] else None
        good_type = int(form['type']) if form['type'] else None

        # 建立初始查询条件query
        query = Q(status__gte=0)

        # 对form内容进行处理，获得所需查询集
        if name:
            goods = Good.objects.filter(good_name__icontains=name, status=1)
            good_codes = []
            for good in goods:
                good_codes.append(good.good_code)
            for item in queryset:
                if item.good_code not in good_codes:
                    unnecessary_goods.append(item.good_code)
        if code:
            query = query & Q(good_code=code)
        if location and location != '0':
            query = query & Q(position=location)
        if status and status != 0:
            query = query & Q(status=status)
        queryset = queryset.filter(query)
        if good_type and good_type != 0:
            goods = Good.objects.filter(good_type_id=good_type, status=1)
            good_codes = []
            for good in goods:
                good_codes.append(good.good_code)
            for item in queryset:
                if item.good_code not in good_codes:
                    unnecessary_goods.append(item.good_code)

    serializer_data = []

    # 序列化查询集
    for item in queryset:
        if item.good_code not in unnecessary_goods:
            serializer_data.append(item.to_json())

    # 自定义分页
    total = len(serializer_data)
    serializer_data = serializer_data[(page - 1) * page_limit:page * page_limit]
    serializer_data.append({'total': total})

    data = {
        "code": 200,
        "result": True,
        "message": "OK",
        "data": serializer_data
    }
    return get_result(data)


@require_GET
def get_good_type_list(request):
    """获取商品类别列表"""
    good_types = GoodType.objects.all()
    good_type_list = [good_type.to_json() for good_type in good_types]
    return get_result({"data": good_type_list})


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
    data = {"total_num": len(goods),
            "good_list": [good.to_json() for good in cur_goods]}  # ！这里还是for循环内部查询了数据库
    return get_result({"data": data})


@require_GET
def get_good_status_list(request):
    """
    获取物资状态列表
    """
    good_status_list = []
    for item in GroupApply.STATUS_TYPE:
        good_status_list.append({'id': item[0], 'status_name': item[1]})
    return get_result({"data": good_status_list})

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


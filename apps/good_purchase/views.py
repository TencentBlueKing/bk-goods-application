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

from apps.good_purchase.models import (Good, GoodType, GroupApply, Withdraw,
                                       WithdrawReason)
from apps.good_purchase.serializers import (CheckWithdrawsSeralizers,
                                            GoodSerializers,
                                            GoodTypeSerializers)
from apps.tools.param_check import (check_param_id, check_param_page,
                                    check_param_size, check_param_str,
                                    get_error_message)
from apps.tools.response import get_result
from config.default import os
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils.datetime_safe import datetime
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
    good_code = good_serializers.validated_data.get("good_code")
    if Good.objects.filter(good_code=good_code, status=1).exists():
        return get_result({"code": 1, "result": False, "message": "商品编码已存在"})
    # 检验商品类型是否存在
    good_type_id = good_serializers.validated_data.get("good_type_id")
    if not GoodType.objects.filter(id=good_type_id).exists():
        return get_result({"code": 1, "result": False, "message": "商品类型不存在"})
    with transaction.atomic():
        Good.objects.create(**good)
    return get_result({"message": "新增商品成功"})


@require_POST
def update_good(request):
    """修改商品信息"""
    good = json.loads(request.body)
    # 参数校验
    good_serializers = GoodSerializers(data=good)
    if not good_serializers.is_valid():
        message = get_error_message(good_serializers)
        return get_result({"code": 1, "result": False, "message": message})
    # 校验id
    good_id = good.get("id", 0)
    if not check_param_id(good_id):
        return get_result({"code": 1, "result": False, "message": "商品id不合法"})
    # 校验商品是否存在
    if not Good.objects.filter(id=good_id, status=1).exists():
        return get_result({"code": 1, "result": False, "message": "商品不存在"})
    # 检验商品编码是否重复(good_code相同，但id不同的商品)
    good_code = good_serializers.validated_data.get("good_code")
    if Good.objects.filter(Q(good_code=good_code) & ~Q(id=good_id) & Q(status=1)).exists():
        return get_result({"code": 1, "result": False, "message": "商品编号已存在"})
    # 校验商品类型是否存在
    good_type_id = good_serializers.validated_data.get("good_type_id")
    if not GoodType.objects.filter(id=good_type_id).exists():
        return get_result({"code": 1, "result": False, "message": "商品类型不存在"})
    # 更新数据
    Good.objects.filter(id=good_id).update(**good, update_time=datetime.now())
    return get_result({"message": "修改商品信息成功"})


@require_GET
def down_good(request):
    """商品下架"""
    good_id = request.GET.get("id", 0)
    # 校验参数
    if not check_param_id(good_id):
        return get_result({"code": 1, "result": False, "message": "good_id参数校验出错"})
    # 校验商品是否存在
    if not Good.objects.filter(id=good_id, status=1).exists():
        return get_result({"code": 1, "result": False, "message": "商品不存在"})
    Good.objects.filter(id=good_id).update(status=0)
    return get_result({"message": "下架商品成功"})


@require_POST
def add_good_type(request):
    """新增商品类型"""
    req = json.loads(request.body)
    # 参数校验
    good_type_serializers = GoodTypeSerializers(data=req)
    if not good_type_serializers.is_valid():
        message = get_error_message(good_type_serializers)
        return get_result({"code": 1, "result": False, "message": message})
    # 验证该商品类型是否存在
    type_name = good_type_serializers.validated_data.get("type_name")
    if GoodType.objects.filter(type_name=type_name).exists():
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


@require_POST
def add_withdraw_apply(request):
    """提交退回物资申请"""
    req = json.loads(request.body)
    username = request.user.username
    check_withdraws_seralizers = CheckWithdrawsSeralizers(data=req)
    if not check_withdraws_seralizers.is_valid():
        message = get_error_message(check_withdraws_seralizers)
        return get_result({"code": 1, "result": False, "message": message})
    ids = check_withdraws_seralizers.validated_data.get("good_ids")
    reason_id = check_withdraws_seralizers.validated_data.get("reason_id")
    position = check_withdraws_seralizers.validated_data.get("position")
    remark = check_withdraws_seralizers.validated_data.get("remark", '')
    good_ids = GroupApply.objects.filter(id__in=ids, status=2, username=username).values_list("id", flat=True)
    if not set(good_ids).issubset(ids):
        return get_result({"code": 1, "result": False, "message": "个人物资不存在，或商品不是正在使用状态"})
    if not WithdrawReason.objects.filter(id=reason_id).exists():
        return get_result({"code": 1, "result": False, "message": "退回原因不存在"})
    # 创建需要批量添加的withdraw数组
    withdraw_list = []
    for good_id in good_ids:
        withdraw = Withdraw(good_apply_id=good_id, username=username, reason_id=reason_id,
                            position=position, remark=remark)
        withdraw_list.append(withdraw)
    with transaction.atomic():
        # 修改个人物资状态
        GroupApply.objects.filter(id__in=list(good_ids)).update(status=1)
        # 批量添加物资退回表
        Withdraw.objects.bulk_create(withdraw_list)
    return get_result({"message": "退回商品申请提交成功"})


@require_GET
def get_withdraw_reason(request):
    """获取所有退库原因"""
    withdraw_reasons = WithdrawReason.objects.all()
    withdraw_reason_list = [reason.to_json() for reason in withdraw_reasons]
    return get_result({"data": withdraw_reason_list})

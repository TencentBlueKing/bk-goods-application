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
import json

from apps.good_apply.models import Apply, Position, Secretary
from apps.good_apply.serializers import ApplySerializers
from apps.tools.param_check import check_param_str, get_error_message
from apps.tools.response import get_result
from blueapps.utils import get_client_by_request
from django.shortcuts import render
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from django.views.decorators.http import require_GET, require_POST


def home(request):
    """
    首页
    """
    return render(request, "index.html")


@require_GET
def get_root_position_list(request):
    """获取一级地区"""
    positions = Position.objects.filter(parent_code__isnull=True)
    position_list = [position.to_json() for position in positions]
    return get_result({"data": position_list})


@require_GET
def get_sub_position_list(request):
    """（根据上级地区代码）获取下级地区"""
    parent_code = request.GET.get('parent_code', None)
    if not check_param_str(parent_code):
        return get_result({'result': False, 'message': '上级地区代码参数不合法'})
    positions = Position.objects.filter(parent_code=parent_code)
    position_list = [position.to_json() for position in positions]
    return get_result({"data": position_list})


@require_GET
def get_leader(request):
    """根据用户username获取组长"""
    username = request.user.username
    client = get_client_by_request(request=request)
    response = client.usermanage.retrieve_user(lookup_field="username",
                                               id=username,
                                               fields="leader")
    result = response.get('result')
    if not result:
        # 请求接口失败，返回请求结果，包括出错信息
        return response
    leaders = [leader.get('username') for leader in response.get('data').get('leader')]  # !默认有一个admin组长
    return get_result({"message": "上传图片成功", "data": ','.join(leaders)})


@require_POST
def submit_apply_list(request):
    """提交物资申请"""
    req = json.loads(request.body)
    apply_list = req.get('apply_list')
    if not isinstance(apply_list, list):
        return get_result({'result': False, 'message': '物资申请列表参数不合法'})
    # 拼接新增数据
    applys = []
    for apply in apply_list:
        # 参数校验
        apply_serializers = ApplySerializers(data=apply)
        if not apply_serializers.is_valid():
            message = get_error_message(apply_serializers)
            return get_result({"code": 1, "result": False, "message": message})
        validated_data = apply_serializers.validated_data
        positions = [validated_data.get('school'), validated_data.get('academy'), validated_data.get('detail_position')]
        apply = Apply(good_code=validated_data.get('good_code'),
                      good_name=validated_data.get('good_name'),
                      num=validated_data.get('num'),
                      require_date=validated_data.get('require_date'),
                      reason=validated_data.get('reason'),
                      position=','.join(positions),
                      apply_user=validated_data.get('apply_user'))
        applys.append(apply)
    # 批量添加物资申请表
    Apply.objects.bulk_create(applys)
    return get_result({"message": "物资申请提交成功"})


def is_secretary(username):
    if Secretary.objects.filter(username=username).exists():
        return True
    return False


@require_GET
def if_admin(request):
    """检验是否为秘书"""
    username = request.user.username
    return get_result({"result": is_secretary(username)})

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
import datetime
import json

from apps.good_apply.models import Apply, Position, Review
from apps.good_apply.serializers import ApplySerializers, IDListSeralizers
from apps.tools.auth_check import (get_users_in_group, is_leader_or_secretary,
                                   is_secretary, sub_users_in_group)
from apps.tools.decorators import check_leader_or_secretary_permission
from apps.tools.param_check import (check_param_page, check_param_size,
                                    check_param_str, get_error_message)
from apps.tools.response import get_result
from blueapps.utils import get_client_by_request
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
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
def get_position_list(request):
    positions = Position.objects.all()
    position_list = [position.to_json() for position in positions]
    return get_result({"data": position_list})


@require_GET
def get_root_position_list(request):
    """获取一级地区"""
    # positions = Position.objects.filter(parent_code__isnull=True)
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
    # 查询蓝鲸平台，单个用户信息-返回组长信息
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


@require_GET
def if_admin(request):
    """检验是否为秘书"""
    username = request.user.username
    return get_result({"result": is_secretary(username)})


@check_leader_or_secretary_permission
@require_POST
def examine_apply(request, leader_or_secretary):
    username = request.user.username
    body = request.body
    body = json.loads(body)
    apply_id_list = body.get('apply_id_list')
    model = body.get('model')
    remark = body.get('remark')

    # 校验数据
    if not check_param_str(remark):
        result = {
            "code": 400,
            "result": False,
            "message": "备注必须为字符串",
            "data": {}
        }
        return get_result(result)

    apply_id_list_serializer = IDListSeralizers(data={'apply_id_list': apply_id_list})

    if not apply_id_list_serializer.is_valid():
        message = get_error_message(apply_id_list_serializer)
        result = {
            "code": 400,
            "result": False,
            "message": message,
            "data": {}
        }
        return get_result(result)

    # 根据不同身份设置不同的审核结果以及身份标识
    if leader_or_secretary == 0:  # 秘书
        reviewer_identity = 1
        review_result = 3
    else:
        reviewer_identity = 0
        if model == 'reject':
            review_result = 3
        elif model == 'agree':
            review_result = 2
    if model == 'reject':  # 拒绝申请：
        review_list = []
        with transaction.atomic():
            applies = Apply.objects.filter(id__in=apply_id_list)
            applies.update(status=review_result)
            for apply_id in apply_id_list:
                # apply_obj = Apply.objects.filter(id=apply_id).first()
                # apply_obj.status = review_result
                # apply_obj.save()
                review_obj = Review(apply_id=apply_id, reviewer=username,
                                    reviewer_identity=reviewer_identity, result=2, reason=remark)
                review_list.append(review_obj)
            Review.objects.bulk_create(review_list)
    elif model == 'agree':  # 同意申请
        review_list = []
        with transaction.atomic():
            applies = Apply.objects.filter(id__in=apply_id_list)
            applies.update(status=review_result)
            for apply_id in apply_id_list:
                # apply_obj = Apply.objects.filter(id=apply_id).first()
                # apply_obj.status = review_result
                # apply_obj.save()
                review_obj = Review(apply_id=apply_id, reviewer=username,
                                    reviewer_identity=reviewer_identity, result=1, reason=remark)
                review_list.append(review_obj)
            Review.objects.bulk_create(review_list)

    if model == 'reject' or model == 'agree':
        result = {
            "code": 200,
            "result": True,
            "message": '审核成功',
            "data": {}
        }
        return get_result(result)


@require_GET
def if_leader_or_secretary(request):
    """是否是秘书/管理员"""
    flag, leader_or_secretary = is_leader_or_secretary(request)
    print('flag={}, leader_or_secretary={}'.format(type(flag), type(leader_or_secretary)))
    return get_result({"result": flag, "data": {'identity': leader_or_secretary}})


@check_leader_or_secretary_permission
def get_apply_users(request, leader_or_secretary):
    """审批页面，获取申请人列表：秘书获取所有/组长获取本组的申请人"""
    if leader_or_secretary == 0:  # 秘书
        users = [{'id': user.get('id'),
                  'username': user.get('username'),
                  'display_name': user.get('display_name')}
                 for user in get_users_in_group(request, group_id=6)]
    else:  # 组长
        users = sub_users_in_group(request, username=request.user.username, group_id=6)
    return get_result({"result": users})


@check_leader_or_secretary_permission
@require_GET
def get_goods_apply(request, leader_or_secretary):
    """
    获取需要审核的物资列表
    """
    if leader_or_secretary == 0:
        # 秘书, 查询审核中
        query = Q(status=2)
        # 可查询的所有人
        user_usernames = [user.get('username') for user in get_users_in_group(request, group_id=6)]
    else:
        # 组长，查询未审核
        query = Q(status=1)
        users = sub_users_in_group(request, username=request.user.username, group_id=6)
        user_usernames = [user.get('username') for user in users]

    # 申请人-查询条件
    apply_user = request.GET.get('apply_user', None)
    if check_param_str(apply_user):
        if apply_user in user_usernames:
            query = query & Q(apply_user=apply_user)
        else:
            return get_result({"code": 1, "result": False, "message": u"您对-{}没有查询权限".format(apply_user)})
    else:
        # 没有选择要查询的申请人
        query = query & Q(apply_user__in=user_usernames)

    # 地点-模糊查询
    position = request.GET.get('position', None)
    if check_param_str(position):
        query = query & Q(position__contains=position)

    # 时间-范围查询
    start_time = request.GET.get('start_time')
    if not start_time:
        start_time = '1970-1-1'
    end_time = request.GET.get('end_time')
    if not end_time:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d')
    query = query & Q(create_time__range=(start_time, end_time))

    # 分页
    page = request.GET.get('page', 1)
    page = check_param_page(page)
    size = request.GET.get('size', 10)
    size = check_param_size(size)

    # 查询
    applys = Apply.objects.filter(query).order_by("-update_time")
    paginator = Paginator(applys, size)
    cur_applys = paginator.get_page(page)

    data = {"total_num": applys.count(),
            "apply_list": [apply.to_json() for apply in cur_applys]}
    return get_result({'data': data})

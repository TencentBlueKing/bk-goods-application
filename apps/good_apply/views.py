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
import os

from apps.good_apply.models import Apply, Position, Review
from apps.good_apply.serializers import (ApplyCheckSerializers,
                                         ApplyPostSerializers,
                                         ApplySerializers, IDListSeralizers,
                                         PositionSerializer)
from apps.tools.auth_check import (get_users_in_group, is_leader_or_secretary,
                                   sub_users_in_group)
from apps.tools.decorators import check_leader_or_secretary_permission
from apps.tools.param_check import (check_param_id, check_param_page,
                                    check_param_size, check_param_str,
                                    get_error_message)
from apps.tools.response import get_result, success_code
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from blueapps.utils import get_client_by_request
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework.decorators import action


def home(request):
    """
    首页
    """
    if os.getenv('BKAPP_DJANGO_CONFIG', 'apply') == 'apply':
        return render(request, "apply_index.html")
    else:
        return render(request, 'index.html')


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    @action(methods=['get'], detail=False)
    def get_root_position_list(self, request):
        """获取一级地区"""
        positions = self.queryset.filter(parent_code__isnull=True)
        position_list = [position.to_json() for position in positions]
        return JsonResponse(success_code(position_list))

    @action(methods=['get'], detail=False)
    def get_sub_position_list(self, request):
        """（根据上级地区代码）获取下级地区"""
        req_data = request.GET
        parent_code = req_data.get('parent_code', None)
        if not check_param_str(parent_code):
            raise BusinessException(StatusEnums.AREA_ERROR)
        positions = Position.objects.filter(parent_code=parent_code)
        position_list = [position.to_json() for position in positions]
        return JsonResponse(success_code(position_list))


class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializers

    def update(self, request, *args, **kwargs):
        if not request.data.get('require_date'):
            require_date = Apply.objects.get(id=request.data['id']).require_date
            request.data['require_date'] = require_date
        if not request.data.get('position'):
            position = Apply.objects.get(id=request.data['id']).position
            request.data['position'] = position
        if not request.data.get('status'):
            status = Apply.objects.get(id=request.data['id']).status
            request.data['status'] = status
        if not request.data.get('apply_user'):
            apply_user = Apply.objects.get(id=request.data['id']).apply_user
            request.data['apply_user'] = apply_user
        if not request.data.get('apply_time'):
            create_time = Apply.objects.get(id=request.data['id']).create_time
            request.data['create_time'] = create_time
        return super().update(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def submit_apply_list(self, request):
        """提交物资申请"""
        req = request.data
        username = request.user.username
        apply_list = req.get('apply_list')
        # flag, leader_or_secretary = is_leader_or_secretary(request)
        flag, leader_or_secretary = (True, 0)
        apply_status = 1
        if leader_or_secretary == 0:
            apply_status = 3
        elif leader_or_secretary == 1:
            apply_status = 2
        if not isinstance(apply_list, list):
            raise BusinessException(StatusEnums.APPLY_GOODS_ERROR)
        # 拼接新增数据
        applys = []
        for apply in apply_list:
            # 参数校验
            apply_serializers = ApplyCheckSerializers(data=apply)
            if not apply_serializers.is_valid():
                message = get_error_message(apply_serializers)
                return get_result({"code": 1, "result": False, "message": message})
            validated_data = apply_serializers.validated_data
            positions = [validated_data.get('school'), validated_data.get('academy'),
                         validated_data.get('detail_position')]
            apply = Apply(good_code=validated_data.get('good_code'),
                          good_name=validated_data.get('good_name'),
                          num=validated_data.get('num'),
                          require_date=validated_data.get('require_date'),
                          reason=validated_data.get('reason'),
                          position=','.join(positions),
                          status=apply_status,
                          apply_user=validated_data.get('apply_user'))
            applys.append(apply)

        # 批量添加物资申请表
        old_apply_ids = list(Apply.objects.values_list('id', flat=True))
        Apply.objects.bulk_create(applys)
        if flag:
            reviews = []
            new_create_apply_ids = Apply.objects.exclude(id__in=old_apply_ids).values_list('id', flat=True)
            if leader_or_secretary == 0:  # 管理员
                for new_create_apply_id in new_create_apply_ids:
                    review = Review(apply_id=new_create_apply_id, reviewer=username, reviewer_identity=2,
                                    result=1, reason="管理员自身提交的申请，无需审核")
                    reviews.append(review)
            elif leader_or_secretary == 1:  # 导员
                for new_create_apply_id in new_create_apply_ids:
                    review = Review(apply_id=new_create_apply_id, reviewer=username, reviewer_identity=1,
                                    result=1, reason="导员自身提交的申请，第一级无需审核")
                    reviews.append(review)
            if reviews:
                Review.objects.bulk_create(reviews)

        return get_result({"message": "物资申请提交成功"})

    def list(self, request, *args, **kwargs):
        """
        获取需要审核的物资列表
        """
        uesrname = request.user.username
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        req_data = request.GET
        if leader_or_secretary == 0:
            # 秘书, 查询审核中
            query = Q(status=2)
            # 可查询的所有人
            user_usernames = [user.get('username') for user in get_users_in_group(request, group_id=6)]
        else:
            # 导员，查询未审核
            query = Q(status=1)
            users = sub_users_in_group(request, username=request.user.username, group_id=6)
            user_usernames = [user.get('username') for user in users]
            user_usernames.append(uesrname)

        # 申请人-查询条件
        apply_user = req_data.get('apply_user', None)
        if check_param_str(apply_user):
            if apply_user in user_usernames:
                query = query & Q(apply_user=apply_user)
            else:
                return get_result({"code": 4009, "result": False, "message": u"您对-{}没有查询权限".format(apply_user)})
        else:
            # 没有选择要查询的申请人
            query = query & Q(apply_user__in=user_usernames)

        # 地点-模糊查询
        position = req_data.get('position', None)
        if check_param_str(position):
            query = query & Q(position__contains=position)

        # 时间-范围查询
        start_time = req_data.get('start_time')
        end_time = req_data.get('end_time')

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
        query = query & Q(create_time__range=(start_time, end_time))

        # 分页
        page = req_data.get('page', 1)
        page = check_param_page(page)
        size = req_data.get('size', 10)
        size = check_param_size(size)

        # 查询
        applys = Apply.objects.filter(query).order_by("-update_time")
        paginator = Paginator(applys, size)
        cur_applys = paginator.get_page(page)

        data = {"total_num": applys.count(),
                "apply_list": [apply.to_json() for apply in cur_applys]}
        return JsonResponse(success_code(data))

    @action(methods=['GET'], detail=False)
    def get_self_good_apply_list(self, request, *args, **kwargs):
        """
        查询自己的物资申请
        """
        sql_str = (
            "select apply.id, apply.good_code, apply.good_name, "
            "apply.create_time as create_time, apply.num, apply.reason, "
            "(case apply.`status` "
            "when 0 then '申请终止' "
            "when 1 then '导员审核中' "
            "when 2 then '管理员审核中' "
            "when 3 then '审核完成' "
            "end) as `status`,"
            "review.reviewer, "
            "(case review.result "
            "when 1 then '通过' "
            "when 2 then '未通过' "
            "end) as `result`,"
            "review.create_time as review_time, review.reason as review_reason "
            "from good_apply_apply apply "
            "left join good_apply_review review "
            "on review.apply_id = apply.id "
            "where apply.apply_user = %s "
            "and apply.create_time between %s and %s "
        )
        params = [request.user.username]
        req_data = request.GET
        # 时间-范围查询
        start_time = req_data.get('start_time')
        end_time = req_data.get('end_time')

        if start_time and end_time:
            if not start_time <= end_time:
                raise ValueError('开始日期不能大于结束日期')

        if not start_time:
            start_time = '1970-1-1'
        params.append(start_time)
        if not end_time:
            end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            end_time = (datetime.datetime.strptime(end_time, "%Y-%m-%d")
                        + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        params.append(end_time)

        # 物品编码、物品名、申请原因模糊查询
        conditions = ('good_code', 'good_name', 'reason')
        for condition in conditions:
            # 查询筛选值
            condition_value = req_data.get(condition, None)
            if check_param_str(condition_value):
                # 新建模糊查询筛选条件
                sql_str = sql_str + u"and apply.{} like '%%{}%%'".format(condition, condition_value)
                # # 参数拼接
                # params.append(condition_value)

        # 审核状态查询
        status = req_data.get('status', None)
        if status and isinstance(status, int):
            sql_str = sql_str + 'and apply.status = {}'.format(status)
        elif status == 0:
            sql_str = sql_str + 'and apply.status = {}'.format(status)

        # 根据id查询
        apply_id = req_data.get('id', None)
        if id and isinstance(apply_id, int):
            sql_str = sql_str + 'and apply.id = {}'.format(apply_id)

        # 分页
        page = req_data.get('page', 1)
        page = check_param_page(page)
        size = req_data.get('size', 10)
        size = check_param_size(size)

        apply_infos = Apply.objects.raw(sql_str, params)
        paginator = Paginator(apply_infos, size)
        cur_applys = paginator.get_page(page)
        apply_list = []
        for apply_info in cur_applys:
            apply_list.append({
                "id": apply_info.id,
                "good_code": apply_info.good_code,
                "good_name": apply_info.good_name,
                "create_time": apply_info.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "num": apply_info.num,
                "reason": apply_info.reason,
                "status": apply_info.status,
                "reviewer": apply_info.reviewer,
                "review_time": apply_info.review_time,
                "review_result": apply_info.result,
                "review_reason": apply_info.review_reason
            })
        return JsonResponse(success_code({"total_num": len(apply_infos), "apply_list": apply_list}))

    @action(methods=['POST'], detail=False)
    def examine_apply(self, request):
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        username = request.user.username
        body = request.data
        apply_id_list = body.get('apply_id_list')
        model = body.get('model')
        remark = body.get('remark')

        # 校验数据
        if not check_param_str(remark):
            raise BusinessException(StatusEnums.REMARK_ERROR)

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
            reviewer_identity = 2
            review_result = 3
        else:
            reviewer_identity = 1
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
            return get_result({"message": "审核成功"})

    @action(methods=['PATCH'], detail=False)
    def update_good_apply(self, request):
        """编辑物资申请"""
        apply = request.data
        apply_id = apply.get("id")
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        # 检查物资申请是否存在且该状态是否还可被修改
        if not Apply.objects.filter(id=apply_id, status=1).exists():
            raise BusinessException(StatusEnums.MODIFY_ERROR)
        # 修改参数校验
        apply_serializers = ApplyPostSerializers(data=apply)
        if not apply_serializers.is_valid():
            message = get_error_message(apply_serializers)
            return get_result({"code": 1, "result": False, "message": message})
        validated_data = apply_serializers.validated_data
        apply = {"good_code": validated_data.get('good_code'),
                 "good_name": validated_data.get('good_name'),
                 "num": validated_data.get('num'),
                 "reason": validated_data.get('reason')}
        # 更新
        Apply.objects.filter(id=apply_id).update(**apply, update_time=datetime.datetime.now())
        return get_result({"message": "修改物资申请信息成功"})

    @action(methods=['PATCH'], detail=False)
    def stop_good_apply(self, request):
        """终止物资申请"""
        req_data = request.data
        apply_id = req_data.get("id")
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        apply = Apply.objects.filter(id=apply_id)
        if not apply.exists():
            raise BusinessException(StatusEnums.NOTFOUND_ERROR)
        if not (apply[0].status == 1 or apply[0].status == 2):
            raise BusinessException(StatusEnums.NODELETE_ERROR)
        apply.update(status=0, update_time=datetime.datetime.now())
        return get_result({"message": "物资申请终止成功"})

    @action(methods=['DELETE'], detail=True)
    def delete_good_apply(self, request, pk):
        """删除物资申请"""

        apply_id = pk
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        apply = Apply.objects.filter(id=apply_id)
        if not apply.exists():
            raise BusinessException(StatusEnums.NOAPPLY_ERROR)
        if apply[0].status == 2:
            raise BusinessException(StatusEnums.DELETE_ERROR)
        apply.delete()
        return get_result({"message": "物资申请删除成功"})

    @action(methods=['GET'], detail=False)
    def get_apply_status(self, request):
        """获取所有申请状态"""
        apply_status_list = []
        for item in Apply.STATUS_TYPE:
            apply_status_list.append({'id': item[0], 'name': item[1]})
        return JsonResponse(success_code(apply_status_list))


@require_GET
def if_leader_or_secretary(request):
    """是否是秘书/管理员"""
    flag, leader_or_secretary = is_leader_or_secretary(request)
    return get_result({"result": flag, "data": {'identity': leader_or_secretary}})


@check_leader_or_secretary_permission
def get_apply_users(request, leader_or_secretary):
    """审批页面，获取申请人列表：秘书获取所有/导员获取本组的申请人"""
    if leader_or_secretary == 0:  # 秘书
        users = [{'id': user.get('id'),
                  'username': user.get('username'),
                  'display_name': user.get('display_name')}
                 for user in get_users_in_group(request, group_id=6)]
    else:  # 导员
        users = sub_users_in_group(request, username=request.user.username, group_id=6)
    return JsonResponse(success_code(users))


def get_leaders_fun(request, username):
    client = get_client_by_request(request=request)
    response = client.usermanage.retrieve_user(lookup_field="username",
                                               id=username,
                                               fields="leader")
    result = response.get('result')
    if not result:
        # 请求接口失败，返回请求结果，包括出错信息
        return response
    leaders = [leader.get('username') for leader in response.get('data').get('leader')]  # !默认有一个admin导员
    return leaders


@require_GET
def get_leader(request):
    """根据用户username获取导员"""
    username = request.user.username
    flag, leader_or_secretary = is_leader_or_secretary(request)
    # 查询蓝鲸平台，单个用户信息-返回组长信息
    leaders = []
    if not flag:
        leaders = get_leaders_fun(request, username)
    elif leader_or_secretary == 1:
        users = sub_users_in_group(request, username=username, group_id=6)
        username = users[0]['username']
        leaders = get_leaders_fun(request, username)
    if leaders:
        return get_result({"message": "获取成功", "data": ','.join(leaders)})
    elif leader_or_secretary == 0:
        return JsonResponse(success_code({}))
    else:
        raise BusinessException(StatusEnums.HANDLE_ERROR)

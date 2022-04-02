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

from apps.good_apply.models import (Apply, OrganizationMember, Position,
                                    Review, Secretary)
from apps.good_apply.serializers import (ApplyCheckSerializers,
                                         ApplyPostSerializers,
                                         ApplySerializers, IDListSeralizers,
                                         OrganizationMemberSerializer,
                                         PositionSerializer)
from apps.tools.auth_check import if_secretary
from apps.tools.param_check import (check_param_id, check_param_page,
                                    check_param_size, check_param_str,
                                    get_error_message)
from apps.tools.response import get_result, success_code
from apps.tools.tool_get_normal_member import tool_get_normal_member
from apps.tools.tool_get_start_end import tool_get_start_end
from apps.tools.tool_paginator import tool_paginator
from apps.tools.tool_valid_user_in_the_org import valid_user_in_the_org
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
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
    """
    地区表视图集
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    @action(methods=['get'], detail=False)
    def get_root_position_list(self, request):
        """获取一级地区"""
        req_data = request.GET
        org_id = req_data.get('org_id', None)
        valid_user_in_the_org(org_id, request.user.username)
        query = Q(parent_code__isnull=True) & Q(org_id=org_id)
        positions = self.queryset.filter(query)
        position_list = [position.to_json() for position in positions]
        return JsonResponse(success_code(position_list))

    @action(methods=['get'], detail=False)
    def get_sub_position_list(self, request):
        """（根据上级地区代码）获取下级地区"""
        req_data = request.GET
        org_id = req_data.get('org_id', None)
        valid_user_in_the_org(org_id, request.user.username)
        parent_code = req_data.get('parent_code', None)
        if not check_param_str(parent_code):
            raise BusinessException(StatusEnums.AREA_ERROR)
        query = Q(parent_code=parent_code) & Q(org_id=org_id)
        positions = Position.objects.filter(query)
        position_list = [position.to_json() for position in positions]
        return JsonResponse(success_code(position_list))


class ApplyViewSet(viewsets.ModelViewSet):
    """
    申请表视图集
    """
    queryset = Apply.objects.all()
    serializer_class = ApplySerializers

    def update(self, request, *args, **kwargs):
        """重写update方法，更新申请时require_date，position，status，apply_user，apply_time非必须传入"""
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
        """
        提交物资申请
        若是普通用户提交申请，则直接生成申请表，状态为管理员审核中
        若是管理员提交申请，则生成申请表，并且状态为已审核，且会生成审核表
        """
        req = request.data
        username = request.user.username
        apply_list = req.get('apply_list')
        org_id = req.get('org_id', None)
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        apply_status = 1
        if flag:
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
                return get_result({"code": 400, "result": False, "message": message})
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
                          apply_user=validated_data.get('apply_user'),
                          org_id=org_id)
            applys.append(apply)

        # 批量添加物资申请表
        old_apply_ids = list(Apply.objects.values_list('id', flat=True))
        Apply.objects.bulk_create(applys)
        if flag:
            reviews = []
            new_create_apply_ids = Apply.objects.exclude(id__in=old_apply_ids).values_list('id', flat=True)
            for new_create_apply_id in new_create_apply_ids:
                review = Review(apply_id=new_create_apply_id, reviewer=username, reviewer_identity=1,
                                result=1, reason="管理员自身提交的申请，无需审核", org_id=org_id)
                reviews.append(review)
            if reviews:
                Review.objects.bulk_create(reviews)

        return get_result({"message": "物资申请提交成功"})

    def list(self, request, *args, **kwargs):
        """
        获取需要审核的物资列表
        """
        req_data = request.GET
        username = request.user.username
        org_id = req_data.get('org_id')
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        # 管理员, 查询审核中
        query = Q(status=1) & Q(org_id=org_id)
        # 可查询的所有普通成员
        normal_member_queryset = tool_get_normal_member(org_id)
        user_usernames = [member.username for member in normal_member_queryset]

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
        start_time, end_time = tool_get_start_end(req_data, 'start_time', 'end_time')
        query = query & Q(create_time__range=(start_time, end_time))

        cur_applys, total_num = tool_paginator(req_data, Apply, query, 'page', 'size')

        data = {"total_num": total_num,
                "apply_list": [apply.to_json() for apply in cur_applys]}
        return JsonResponse(success_code(data))

    @action(methods=['GET'], detail=False)
    def get_self_good_apply_list(self, request, *args, **kwargs):
        """
        查询自己的物资申请
        """
        username = request.user.username
        sql_str = (
            "select apply.id, apply.good_code, apply.good_name, "
            "apply.create_time as create_time, apply.num, apply.reason, "
            "(case apply.`status` "
            "when 0 then '申请终止' "
            "when 1 then '管理员审核中' "
            "when 2 then '审核完成' "
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
        params = [username]
        req_data = request.GET
        org_id = req_data.get('org_id', None)
        valid_user_in_the_org(org_id, username)
        sql_str = sql_str + 'and apply.org_id = {}'.format(org_id)
        # 时间-范围查询
        start_time, end_time = tool_get_start_end(req_data, 'start_time', 'end_time')
        params.append(start_time)
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
        if status and isinstance(status, str):
            status = int(status)
        if isinstance(status, int):
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
        """审核申请"""
        body = request.data
        org_id = body.get('org_id', None)
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
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

        reviewer_identity = 1
        review_result = 2

        if model == 'reject':  # 拒绝申请：
            review_list = []
            with transaction.atomic():
                # 更新申请表状态
                applies = Apply.objects.filter(id__in=apply_id_list, org_id=org_id)
                applies.update(status=review_result)
                # 创建对应审核表
                for apply_id in apply_id_list:
                    review_obj = Review(apply_id=apply_id, reviewer=username,
                                        reviewer_identity=reviewer_identity, result=2, reason=remark, org_id=org_id)
                    review_list.append(review_obj)
                Review.objects.bulk_create(review_list)
        elif model == 'agree':  # 同意申请
            review_list = []
            with transaction.atomic():
                # 更新申请表状态
                applies = Apply.objects.filter(id__in=apply_id_list, org_id=org_id)
                applies.update(status=review_result)
                # 创建对应审核表
                for apply_id in apply_id_list:
                    review_obj = Review(apply_id=apply_id, reviewer=username,
                                        reviewer_identity=reviewer_identity, result=1, reason=remark, org_id=org_id)
                    review_list.append(review_obj)
                Review.objects.bulk_create(review_list)

        if model == 'reject' or model == 'agree':
            return get_result({"message": "审核成功"})

    @action(methods=['PATCH'], detail=False)
    def update_good_apply(self, request):
        """编辑物资申请"""
        apply = request.data
        apply_id = apply.get("id")
        org_id = apply.get('org_id', None)
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        # 检查物资申请是否存在且该状态是否还可被修改
        if not Apply.objects.filter(id=apply_id, status=1, org_id=org_id).exists():
            raise BusinessException(StatusEnums.MODIFY_ERROR)
        # 修改参数校验
        apply_serializers = ApplyPostSerializers(data=apply)
        if not apply_serializers.is_valid():
            message = get_error_message(apply_serializers)
            return get_result({"code": 400, "result": False, "message": message})
        validated_data = apply_serializers.validated_data
        apply = {"good_code": validated_data.get('good_code'),
                 "good_name": validated_data.get('good_name'),
                 "num": validated_data.get('num'),
                 "reason": validated_data.get('reason')}
        # 更新
        Apply.objects.filter(id=apply_id, org_id=org_id).update(**apply, update_time=datetime.datetime.now())
        return get_result({"message": "修改物资申请信息成功"})

    @action(methods=['PATCH'], detail=False)
    def stop_good_apply(self, request):
        """终止物资申请"""
        req_data = request.data
        apply_id = req_data.get("id")
        org_id = req_data.get('org_id')
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        apply = Apply.objects.filter(id=apply_id, org_id=org_id)
        if not apply.exists():
            raise BusinessException(StatusEnums.NOTFOUND_ERROR)
        if not (apply[0].status == 1):
            raise BusinessException(StatusEnums.NODELETE_ERROR)
        apply.update(status=0, update_time=datetime.datetime.now())
        return get_result({"message": "物资申请终止成功"})

    @action(methods=['DELETE'], detail=True)
    def delete_good_apply(self, request, pk, org_id):
        """删除物资申请"""
        apply_id = pk
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.APPLY2_GOODS_ERROR)
        apply = Apply.objects.filter(id=apply_id, org_id=org_id)
        if not apply.exists():
            raise BusinessException(StatusEnums.NOAPPLY_ERROR)
        if apply[0].status == 1:
            raise BusinessException(StatusEnums.DELETE_ERROR)
        apply.delete()
        return get_result({"message": "物资申请删除成功"})

    @action(methods=['GET'], detail=False)
    def get_apply_status(self, request):
        """获取所有申请状态"""
        req_data = request.GET
        username = request.user.username
        org_id = req_data.get('org_id', None)
        valid_user_in_the_org(org_id, username)
        apply_status_list = []
        for item in Apply.STATUS_TYPE:
            apply_status_list.append({'id': item[0], 'name': item[1]})
        return JsonResponse(success_code(apply_status_list))


class OrganizationMemberViewSet(viewsets.ModelViewSet):
    """
    组成员表视图集
    """
    queryset = OrganizationMember.objects.all()
    serializer_class = OrganizationMemberSerializer

    @action(methods=['GET'], detail=False)
    def get_apply_users(self, request):
        """审批页面，获取可管理人员"""
        req_data = request.GET
        org_id = req_data.get('org_id')
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        # 根据用户名和组id查秘书表，查看用户是否为此组秘书

        query = Q(username=username)
        query = query & Q(org_id=org_id)
        sec_org = Secretary.objects.filter(query)
        if not sec_org:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        normal_persons = tool_get_normal_member(org_id)

        users = [
            {
                'id': person.id,
                'username': person.username
            }
            for person in normal_persons
        ]
        return JsonResponse(success_code(users))

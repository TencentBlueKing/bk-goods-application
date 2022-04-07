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
import os

from apps.good_apply.models import (Apply, ApplyToOrg, Organization,
                                    OrganizationMember, Position, Review,
                                    Secretary)
from apps.good_apply.serializers import (ApplyCheckSerializers,
                                         ApplyPostSerializers,
                                         ApplySerializers,
                                         ApplyToOrgExamineSerializer,
                                         ApplyToOrgSerializer,
                                         IDListSeralizers,
                                         OrganizationMemberSerializer,
                                         OrgIDSerializer, PositionSerializer,
                                         SecretaryAddSecretarySerializer,
                                         SecretaryPermissionTransferSerializer)
from apps.good_apply.tasks import send_email
from apps.good_purchase.serializers import MemberIDListSerializer
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
from blueapps.account.models import User, UserProperty
from blueapps.conf import settings
from blueapps.utils import get_client_by_request
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
    def get_org_users(self, request):
        """获取当前所在组所有成员"""
        req_data = request.GET
        org_id = req_data.get('org_id')
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        # 获取其中一个组的成员
        queryset = self.queryset.filter(org_id=org_id)
        users = [user.to_json() for user in queryset]
        return JsonResponse(success_code(users))

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

    @action(methods=['POST'], detail=False)
    def add_member_to_org(self, request):
        """添加组成员"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        # 参数校验
        member_id_list = request.data.get('member_id_list')
        member_id_list_serializer = MemberIDListSerializer(data={
            'member_id_list': member_id_list
        })
        if not member_id_list_serializer.is_valid():
            message = get_error_message(member_id_list_serializer)
            return get_result({"code": 400, "result": False, "message": message})

        # 批量创建组成员
        create_list = []
        for member_id in member_id_list:
            member_name = User.objects.filter(id=member_id).username
            # 判断用户是否已经再组中
            if OrganizationMember.objects.filter(org_id=org_id, username=member_name).exists():
                raise BusinessException(StatusEnums.USER_EXIST_ERROR)
            create_list.append(OrganizationMember(username=member_name, org_id=org_id))
        OrganizationMember.objects.bulk_create(create_list)
        return JsonResponse(success_code('操作成功'))

    @action(methods=['get'], detail=False)
    def get_all_group(self, request):
        """获取所有组接口"""
        queryset = Organization.objects.all()
        """取出所有组信息"""
        group_list = [group.to_json() for group in queryset]
        return JsonResponse(success_code(group_list))

    @action(methods=['get'], detail=False)
    def check_user_if_groupmber(self, request):
        """检查用户是否在组成员表内"""
        username = request.user.username
        if not OrganizationMember.objects.filter(username=username).exists():
            raise BusinessException(StatusEnums.USER_NOMEMBER_ERROR)
        return get_result({"message": "用户已有存在组"})

    @action(methods=['post'], detail=False)
    def get_all_groupmber(self, request):
        """获取用户表所有成员"""
        req = request.data
        org_id = req.get('org_id')
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        # 管理员获取除了当前组内其他的用户表中的成员
        queryset = OrganizationMember.objects.exclude(org_id=org_id)
        groupmber_list = [groupmber.to_json() for groupmber in queryset]
        return JsonResponse(success_code(groupmber_list))

    @action(methods=['POST'], detail=False)
    def delete_member_to_org(self, request):
        """删除组成员"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        username = request.user.username
        valid_user_in_the_org(org_id, username)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        # 参数校验
        member_id_list = request.data.get('member_id_list')
        member_id_list_serializer = MemberIDListSerializer(data={
            'member_id_list': member_id_list
        })
        if not member_id_list_serializer.is_valid():
            message = get_error_message(member_id_list_serializer)
            return get_result({"code": 400, "result": False, "message": message})
        for member_id in member_id_list:
            member_name = User.objects.filter(id=member_id).username
            # 判断用户是否已经在组中
            if OrganizationMember.objects.filter(org_id=org_id, username=member_name).exists():
                raise BusinessException(StatusEnums.USER_EXIST_ERROR)
            OrganizationMember.objects.filter(org_id=org_id, username=username).delete()
        return JsonResponse(success_code('操作成功'))


class ApplyToOrgViewSet(viewsets.ModelViewSet):
    """
    申请入组表视图集
    """
    queryset = ApplyToOrg.objects.all()
    serializer_class = ApplyToOrgSerializer

    def list(self, request, *args, **kwargs):
        """获取入组申请"""
        req_data = request.GET
        org_id = req_data.get('org_id')
        username = request.user.username
        flag = if_secretary(request, org_id)
        if not flag:
            # 普通用户, 查询审核中
            query = Q(status=1) & Q(org_id=org_id)

            query = query & Q(create_user=username)

            # 时间-范围查询
            start_time, end_time = tool_get_start_end(req_data, 'start_time', 'end_time')
            query = query & Q(create_time__range=(start_time, end_time))
        else:
            # 管理员, 查询审核中
            query = Q(status=1) & Q(org_id=org_id)

            # 申请人-查询条件
            apply_user = req_data.get('apply_user', None)
            query = query & Q(create_user=apply_user)

            # 地点-模糊查询
            position = req_data.get('position', None)
            if check_param_str(position):
                query = query & Q(position__contains=position)

            # 时间-范围查询
            start_time, end_time = tool_get_start_end(req_data, 'start_time', 'end_time')
            query = query & Q(create_time__range=(start_time, end_time))

        cur_applys, total_num = tool_paginator(req_data, ApplyToOrg, query, 'page', 'size')
        data = {"total_num": total_num,
                "apply_list": [apply.to_json() for apply in cur_applys]}
        return JsonResponse(success_code(data))

    @action(methods=['POST'], detail=False)
    def examine_apply(self, request):
        """审核入组申请"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        username = request.user.username
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        apply_id_list = request.data.get('apply_id_list')
        review_result = request.data.get('review_result')

        # 参数校验
        apply_serializer = ApplyToOrgExamineSerializer(data={
            'apply_id_list': apply_id_list,
            'review_result': review_result
        })
        if not apply_serializer.is_valid():
            message = get_error_message(apply_serializer)
            return get_result({"code": 400, "result": False, "message": message})
        create_list = []
        member_email_list = []
        for apply_id in apply_id_list:
            apply_obj = ApplyToOrg.objects.filter(id=apply_id, org_id=org_id).first()
            if review_result == 0:  # 拒绝申请
                apply_obj.status = 3
                apply_obj.update_user = username
                review_result_ch = '申请失败'
                # 获取申请人的用户id以获取用户的email地址
                member_id = User.objects.filter(username=apply_obj.create_user).first().id
                member_email = UserProperty.objects.filter(user_id=member_id, key='email').first().value
                if not member_email:
                    continue
                member_email_list.append(member_email)
            elif review_result == 1:  # 同意申请
                review_result_ch = '申请成功'
                apply_obj.status = 2
                apply_obj.update_user = username
                create_list.append(OrganizationMember(username=apply_obj.create_user, org_id=org_id))
                # 获取申请人的用户id以获取用户的email地址
                member_id = User.objects.filter(username=apply_obj.create_user).first().id
                member_email = UserProperty.objects.filter(user_id=member_id, key='email').first().value
                if not member_email:
                    continue
                member_email_list.append(member_email)
            if create_list:
                OrganizationMember.objects.bulk_create(create_list)  # 组批量增加成员
            if member_email_list:
                org_name = Organization.objects.filter(id=org_id).first().group_name
                send_email.delay(receiver=member_email_list, title='审核通知'
                                 , content='你加入{org}的申请已审核，结果为{result}'.format(org=org_name
                                                                               , result=review_result_ch))
            return JsonResponse(success_code('审批成功'))

    @action(methods=['post'], detail=False)
    def approval_user_groupmber(self, request):
        """申请加入组接口"""
        req = request.data
        username = request.user.username
        org_id = req.get("org_id")
        if not OrganizationMember.objects.filter(username=username, org_id=org_id).exists():
            if not ApplyToOrg.objects.filter(create_user=username, apply_group_id=org_id).exists():
                ApplyToOrg.objects.create(create_user=username, apply_group_id=org_id, status=1)
                return get_result({"message": "已成功申请加入该组！"})
            return get_result({"message": "已申请，无须重复申请！"})
        return get_result({"message": "你已经在该组当中，无需再次申请"})


class SecretaryViewSet(viewsets.ModelViewSet):
    """
    管理员表视图集
    """
    queryset = Secretary.objects.all()

    @action(methods=['GET'], detail=False)
    def get_org_secretary(self, request):
        """获取秘书"""
        # 身份校验
        org_id = request.data.get('org_id')
        username = request.user.username
        if not org_id:  # 获取所有秘书
            secs = [sec.to_json() for sec in self.queryset]
            return JsonResponse(success_code(secs))
        else:  # 获取一个组秘书
            valid_user_in_the_org(org_id, username)
            queryset = self.queryset.filter(org_id=org_id)
            secs = [sec.to_json() for sec in queryset]
            return JsonResponse(success_code(secs))

    @action(methods=['POST'], detail=False)
    def permission_transfer(self, request):
        """权限转移"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        username = request.user.username
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        old_secretary_id = request.user.id
        new_secretary_id = request.data.get('new_secretary_id', None)

        # 参数校验
        sec_serializer = SecretaryPermissionTransferSerializer(data={
            'old_secretary_id': old_secretary_id,
            'new_secretary_id': new_secretary_id
        })

        if not sec_serializer.is_valid():
            message = get_error_message(sec_serializer)
            return get_result({"code": 400, "result": False, "message": message})

        old_secretary_name = username
        new_secretary_name = User.objects.filter(id=new_secretary_id).first().username
        # 检查与添加身份的用户是否已经是管理员
        if Secretary.objects.filter(username=new_secretary_name, org_id=org_id).exists():
            raise BusinessException(StatusEnums.SECRETARY_EXIST_ERROR)
        Secretary.objects.filter(username=old_secretary_name, org_id=org_id).delete()  # 删除原有管理员身份
        Secretary.objects.create(username=new_secretary_name, org_id=org_id)  # 赋予用户管理员身份
        return JsonResponse(success_code('转移成功'))

    @action(methods=['POST'], detail=False)
    def permission_release(self, request):
        """辞去管理员"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        username = request.user.username
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        # 查看组管理员剩余数量
        if Secretary.objects.filter(org_id=org_id).count() == 1:
            raise BusinessException(StatusEnums.SECRETARY_LACK_ERROR)

        Secretary.objects.filter(username=username, org_id=org_id).delete()  # 删除原有管理员身份
        return JsonResponse(success_code('辞去管理员成功'))

    @action(methods=['POST'], detail=False)
    def add_secretary(self, request):
        """增加管理员"""
        # 身份校验
        org_id = request.data.get('org_id')
        # 验证是否蓝鲸内部组
        if org_id in settings.INNER_LIST:
            raise BusinessException(StatusEnums.INNER_CURD_ERROR)
        flag = if_secretary(request, org_id)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)

        new_secretary_id = request.data.get('new_secretary_id')
        sec_serializer = SecretaryAddSecretarySerializer(data={
            'new_secretary_id': new_secretary_id
        })
        # 参数校验
        if not sec_serializer.is_valid():
            message = get_error_message(sec_serializer)
            return get_result({"code": 400, "result": False, "message": message})
        new_secretary_name = User.objects.filter(id=new_secretary_id).first().username
        # 检查用户是否已在组
        valid_user_in_the_org(org_id, new_secretary_name)
        # 检查与添加身份的用户是否已经是管理员
        if Secretary.objects.filter(username=new_secretary_name, org_id=org_id).exists():
            raise BusinessException(StatusEnums.SECRETARY_EXIST_ERROR)
        Secretary.objects.create(username=new_secretary_name, org_id=org_id)  # 赋予用户管理员身份
        return JsonResponse(success_code('新增管理员成功'))


class OrganizationViewSet(viewsets.ModelViewSet):

    @action(methods=['post'], detail=False)
    def create_group(self, request):
        """创建"""
        username = request.user.username
        req = request.data
        group_name = req.get("group_name")
        if not Organization.objects.filter(group_name=group_name).exists():
            Organization.objects.create(group_name=group_name)
            org_id = Organization.objects.filter(group_name=group_name).first().id
            Secretary.objects.create(username=username, org_id=org_id)
            OrganizationMember.objects.create(username=username, org_id=org_id)
            return get_result({"message": "创建组成功"})
        raise BusinessException(StatusEnums. GROUP_ISEXISTS_ERROR)

    @action(methods=['get'], detail=False)
    def get_all_userin_groupid(self, request):
        """获取用户所有所在组接口"""
        username = request.user.username
        # 根据用户名获取他所在的组成员表查询出来
        group_user_list = OrganizationMember.objects.filter(username=username)
        group_list = []
        for group_user in group_user_list:
            org_id = OrganizationMember.objects.filter(username=group_user.username, id=group_user.id).first().org_id
            group = Organization.objects.filter(id=org_id).first()
            group_list.append(group.to_json())
        return JsonResponse(success_code(group_list))

    @action(methods=['post'], detail=False)
    def quit_group(self, request):
        """用户退出组接口"""
        req = request.data
        username = request.user.username
        org_id = req.get("org_id")
        valid_user_in_the_org(org_id, request.user.username)
        if Secretary.objects.filter(username=username):
            return get_result({"message": "管理员无法退组，请转交管理员身份再执行相关操作"})
        OrganizationMember.objects.filter(username=username, org_id=org_id).delete()
        Apply.objects.filter(apply_user=username, org_id=org_id).delete()
        # GoodApply.objects.filter(username=username, org_id=org_id).delete()
        return get_result({"message": "退出组成功"})

    @action(methods=['post'], detail=False)
    def inner_group(self, request):
        """拉取蓝鲸用户管理系统用户"""
        # TODO: 最高权限校验
        client = get_client_by_request(request=request)
        org_id = request.data.get('org_id', None)
        # 查询组内用户信息
        if not org_id:  # 更新整个内部列表
            inner_list = settings.INNER_LIST
        else:  # 更新单个组
            if org_id in settings.INNER_LIST:
                inner_list = [org_id]
            else:
                raise BusinessException(StatusEnums.ORG_NOT_IN_INNER_ERROR)
        existed_list = Organization.objects.values_list("id", flat=True)  # 系统目前已存在组
        for bk_usermanagement_org_id in inner_list:
            if bk_usermanagement_org_id not in existed_list:  # 若此组还不在申请系统，则先创建组
                response_get_org_info = client.usermanage.retrieve_department(id=bk_usermanagement_org_id)
                org_name = response_get_org_info.get('data').get('name')
                Organization.objects.create(id=bk_usermanagement_org_id, group_name=org_name)
            # 同步组成员信息
            response = client.usermanage.list_department_profiles(id=bk_usermanagement_org_id)
            if not response.get('result'):
                raise BusinessException((5004, response.get('message')))
            users_list = response.get('data').get('results')  # 组内用户列表
            secretary_dict = users_list[0].get('leader')
            secretary_list = list()
            for leader in secretary_dict:
                secretary_list.append(leader.get('username'))
            for user in users_list:
                # 判断用户是否已在组内
                if OrganizationMember.objects.filter(org_id=bk_usermanagement_org_id,
                                                     username=user.get('username')).exists():
                    continue
                OrganizationMember.objects.create(org_id=bk_usermanagement_org_id, username=user.get('username'))
                if user.get('username') in secretary_list:  # 管理员
                    Secretary.objects.create(org_id=org_id, username=user.get('username'))
        return get_result({"message": "内部组成员已存入"})


def add_org_id_to_inner_list(request):
    """添加组id进内部列表"""
    # 参数校验
    org_id_list = json.loads(request.body).get('org_id_list', None)
    org_id_serializer = OrgIDSerializer(data={
        'org_id_list': org_id_list
    })
    if not org_id_serializer.is_valid():
        message = get_error_message(org_id_serializer)
        return get_result({"code": 400, "result": False, "message": message})
    settings.INNER_LIST += org_id_list

    # 防止存在重复组id
    settings.INNER_LIST = set(settings.INNER_LIST)
    settings.INNER_LIST = list(settings.INNER_LIST)
    return JsonResponse(success_code('更新内部列表成功'))


def delete_org_id_from_inner_list(request):
    """内部列表删除某组id"""
    # 参数校验
    org_id_list = json.loads(request.body).get('org_id_list', None)
    org_id_serializer = OrgIDSerializer(data={
        'org_id_list': org_id_list
    })
    if not org_id_serializer.is_valid():
        message = get_error_message(org_id_serializer)
        return get_result({"code": 400, "result": False, "message": message})
    settings.INNER_LIST = list(set(settings.INNER_LIST) - set(org_id_list))

    # 防止存在重复组id
    settings.INNER_LIST = set(settings.INNER_LIST)
    settings.INNER_LIST = list(settings.INNER_LIST)
    return JsonResponse(success_code('更新内部列表成功'))


# TODO: 测试celery
# def test(request):
    # 测试获取组成员信息
    # client = get_client_by_request(request=request)
    # response = client.usermanage.list_department_profiles(id=6)
    # users_list = response.get('data').get('results')
    # leader_dict = users_list[0].get('leader')
    # leader_list = list()
    # for leader in leader_dict:
    #     leader_list.append(leader.get('username'))
    # data = users_list[0].get('username')

    # 测试获取组详细信息
    # client = get_client_by_request(request=request)
    # response = client.usermanage.retrieve_department(id=6)
    #
    # data = response.get('data').get('name')
    # return get_result({'data': data})

    # 测试celery
    # receiver_list = ['790795324@qq.com']
    # receiver_str = ','.join(receiver_list)
    # client = get_client_by_request(request=request)
    # client.cmsi.send_mail(title='testview', content='testview', receiver=receiver_str)

    # client = get_client_by_request(request=request)
    # send_email.delay(client=client, receiver_list=['790795324@qq.com'], title='testdelay', content='testdelay')

    # return get_result({'data': '已发送'})

    # 测试拉人
    # client = get_client_by_request(request=request)
    # existed_list = Organization.objects.values_list("id", flat=True)  # 系统目前已存在组
    # inner_list = [6]
    # for bk_usermanagement_org_id in inner_list:
    #     if bk_usermanagement_org_id not in existed_list:  # 若此组还不在申请系统，则先创建组
    #         response_get_org_info = client.usermanage.retrieve_department(id=bk_usermanagement_org_id)
    #         org_name = response_get_org_info.get('data').get('name')
    #         Organization.objects.create(id=bk_usermanagement_org_id, group_name=org_name)
    #     # 同步组成员信息
    #     response = client.usermanage.list_department_profiles(id=bk_usermanagement_org_id)
    #     if not response.get('result'):
    #         raise BusinessException((5004, response.get('message')))
    #     users_list = response.get('data').get('results')  # 组内用户列表
    #     secretary_dict = users_list[0].get('leader')
    #     secretary_list = list()
    #     for leader in secretary_dict:
    #         secretary_list.append(leader.get('username'))
    #     for user in users_list:
    #         # 判断用户是否已在组内
    #         if OrganizationMember.objects.filter(org_id=bk_usermanagement_org_id,
    #                                              username=user.get('username')).exists():
    #             continue
    #         OrganizationMember.objects.create(org_id=bk_usermanagement_org_id, username=user.get('username'))
    #         if user.get('username') in secretary_list:  # 管理员
    #             Secretary.objects.create(org_id=bk_usermanagement_org_id, username=user.get('username'))
    #
    # return get_result({'data': '已成功'})

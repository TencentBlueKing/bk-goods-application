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
import json
import uuid
from datetime import datetime
from tempfile import NamedTemporaryFile

from apps.good_purchase.models import (Cart, Good, GoodType, GroupApply,
                                       UserInfo, Withdraw, WithdrawReason)
from apps.good_purchase.serializers import (CartSerializer,
                                            CheckWithdrawsSeralizers,
                                            ConfirmReceiptSerializer,
                                            GoodSerializers,
                                            GoodTypeSerializers,
                                            GroupApplySerializers,
                                            UserInfoCheckSerializer,
                                            UserInfoSerializer,
                                            WithdrawReasonSerializer,
                                            WithdrawSerializer,
                                            personalFormSerializer,
                                            personalSerializer)
from apps.tools.auth_check import is_leader_or_secretary
from apps.tools.decorators import check_secretary_permission
from apps.tools.param_check import (check_apply_update_param, check_param_id,
                                    check_param_str, get_error_message)
from apps.tools.response import get_cart_result, get_result, success_code
from apps.tools.tool_delpic import tool_delpic
from apps.tools.tool_paginator import tool_paginator
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from bkstorages.backends.bkrepo import BKRepoStorage
from config.default import os
from django.core.files.base import File
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.decorators import action


@require_POST
def upload_img(request):
    """上传图片"""
    req = json.loads(request.body)
    img_obj = req.get("img")
    file_type = req.get("img_type")
    # 生成随机数命名图片
    file_name = str(uuid.uuid4()) + '.' + file_type
    # 判断文件夹是否存在
    dir_path = 'good_purchase'
    if not os.path.exists(dir_path):
        # os.mkdir(dir_path)
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, file_name)

    storage = BKRepoStorage()

    # 写入图片
    # with open(file_path, 'wb') as f:
    #     f.write(base64.b64decode(img_obj))

    with NamedTemporaryFile() as fp:
        fp.write(base64.b64decode(img_obj))
        fp.flush()
        f = File(fp)
        storage.save(file_path, f)
    # pic_url = settings.BK_BACK_URL + '/media/good_purchase/' + file_name
    pic_url = storage.url(file_path)
    return get_result({"message": "上传图片成功", "data": {"pic_url": pic_url}})


class WithdrawReasonViewSet(viewsets.ModelViewSet):
    queryset = WithdrawReason.objects.all()
    serializer_class = WithdrawReasonSerializer

    def list(self, request, *args, **kwargs):
        withdraw_reason_list = [reason.to_json() for reason in self.queryset]
        return JsonResponse(success_code(withdraw_reason_list))


class WithdrawViewSet(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer

    @action(methods=['POST'], detail=False)
    def add_withdraw_apply(self, request):
        """提交退回物资申请"""
        req = request.data
        username = request.user.username
        check_withdraws_seralizers = CheckWithdrawsSeralizers(data=req)
        if not check_withdraws_seralizers.is_valid():
            message = get_error_message(check_withdraws_seralizers)
            return get_result({"code": 7400, "result": False, "message": message})
        ids = check_withdraws_seralizers.validated_data.get("good_ids")
        reason_id = check_withdraws_seralizers.validated_data.get("reason_id")
        province = check_withdraws_seralizers.validated_data.get("province", None)
        city = check_withdraws_seralizers.validated_data.get("city", None)
        if province and (province != '0' and province != 0):
            if not city or city == '0' or city == 0:
                position = province
            else:
                position = province + '/' + city
        else:
            position = '无'
        remark = check_withdraws_seralizers.validated_data.get("remark", '')
        good_ids = GroupApply.objects.filter(id__in=ids, status=2, username=username).values_list("id", flat=True)
        if not set(ids).issubset(good_ids):
            raise BusinessException(StatusEnums.SENDBACK_ERROR)
        if not WithdrawReason.objects.filter(id=reason_id).exists():
            raise BusinessException(StatusEnums.DRAWBACK_ERROR)
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


@check_secretary_permission
@require_POST
def del_pics(request):
    outcome = tool_delpic(request)
    return outcome


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def list(self, request, *args, **kwargs):
        user_info = {
            'id': self.queryset.filter(username=request.user.username).first().id,
            'username': request.user.username,
            'phone': self.queryset.filter(username=request.user.username).first().phone,
            'position': self.queryset.filter(username=request.user.username).first().position,
            'isScretary': False,
            'isLeader': False
        }
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if flag:
            if leader_or_secretary == 0:
                user_info['isScretary'] = True
            elif leader_or_secretary == 1:
                user_info['isLeader'] = True
        return JsonResponse(success_code(user_info))

    @action(methods=['post'], detail=False)
    def edit_user_info(self, request):
        username = request.user.username  # 获取用户名
        if not UserInfo.objects.filter(username=username).exists():
            raise BusinessException(StatusEnums.USER_NOT_EXIST_ERROR)
        req = request.data
        phone = req.get('phone')
        position = req.get('position')
        user_info = {
            'username': username,
            'phone': phone,
            'position': position
        }
        user_info_serializer = UserInfoCheckSerializer(data=user_info)
        if user_info_serializer.is_valid():  # 参数校验
            UserInfo.objects.filter(username=username).update(
                phone=user_info.get('phone'), position=user_info.get('position'))
            return get_result({'code': 200, 'message': '修改成功'})
        err_msg = get_error_message(user_info_serializer)
        return get_result({'result': False, 'message': err_msg})


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False)
    def get_shopping_cart(self, request):
        """
        获取购物车信息
        """
        username = request.user
        good_list = Cart.objects.filter(username=username)
        if not good_list.exists():
            raise BusinessException(StatusEnums.BLANK_ERROR)
        cart_list = get_cart_result(good_list, source="shop")
        return JsonResponse(success_code(cart_list))

    @action(methods=['post'], detail=False)
    def delete_cart_goods(self, request):
        """
        删除购物车中物资
        """
        username = request.user
        req = request.data
        cart_id_list = req.get("cartIdList")
        if not isinstance(cart_id_list, list):
            cart_all_id = Cart.objects.filter(username=username).values_list("id", flat=True)
            if not set(cart_id_list).issubset(set(cart_all_id)):
                raise BusinessException(StatusEnums.CART_ADX_ERROR)
        if not Cart.objects.filter(id__in=cart_id_list, username=username).exists():
            raise BusinessException(StatusEnums.CART_NULL_ERROR)
        Cart.objects.filter(id__in=cart_id_list).delete()
        return get_result({"code": 200, "message": "删除成功"})

    @action(methods=['POST'], detail=False)
    def update_cart_goods(self, request):
        """
        更新购物车物资数量信息
        """
        req = request.data
        update_goods_list = req.get("goodsList")
        if isinstance(update_goods_list, list):
            update_goods_ids = []
            for update_goods in update_goods_list:
                update_goods_ids.append(update_goods["id"])
            cart_all_id = Cart.objects.values_list("id", flat=True)
            if not set(update_goods_ids).issubset(set(cart_all_id)):
                raise BusinessException(StatusEnums.CART_UPDATE_ERROR)
            all_goods = []
            for good in update_goods_list:
                temp_good = Cart.objects.get(id=good["id"])
                temp_good.num = int(good["num"])
                temp_good.update_time = datetime.now()
                all_goods.append(temp_good)
            Cart.objects.bulk_update(all_goods, ['num', 'update_time'])
        else:
            raise BusinessException(StatusEnums.CART_NUM_ERROR)
        return get_result({"code": 200, "message": "修改成功"})

    @action(methods=['POST'], detail=False)
    def add_cart_goods(self, request):
        """
        物资加入购物车物
        """
        req = request.data
        good_info = req.get("goodInfo")
        username = request.user
        if isinstance(good_info['num'], int) and good_info['num'] > 0:
            temp_good = Cart.objects.filter(good_id=good_info["id"], username=username)
        else:
            raise BusinessException(StatusEnums.CART_NUM_ERROR)
        if temp_good.exists():
            num = int(temp_good[0].num) + int(good_info["num"])
            Cart.objects.filter(good_id=good_info["id"]).update(num=num, update_time=datetime.now())
        else:
            Cart.objects.create(good_id=good_info['id'], username=username, num=good_info['num'])
        return get_result({"code": 200, "message": "物资成功加入购物车"})


class GroupApplyViewSet(viewsets.ModelViewSet):
    queryset = GroupApply.objects.all()
    serializer_class = GroupApplySerializers

    @action(methods=['get'], detail=False)
    def get_group_apply(self, request):
        """
        获取组内物资信息
        """
        apply_list = GroupApply.objects.filter(status=4)
        if not apply_list.exists():
            return get_result({"code": 200, "data": [], "message": "申请状态为购买中的列表为空"})
        cart_list = get_cart_result(apply_list, source="apply")
        return get_result({"code": 200, "data": cart_list, "message": "获取成功"})

    @action(methods=['post'], detail=False)
    def delete_group_apply(self, request):
        """
        删除组内物资
        """
        req = request.data
        apply_id = req.get("applyId")
        if not check_param_id(apply_id):
            raise BusinessException(StatusEnums.CART_ADX_ERROR)
        try:
            GroupApply.objects.get(id=apply_id).delete()
        except GroupApply.DoesNotExist:
            raise BusinessException(StatusEnums.CART_DELETE_ERROR)
        return get_result({"code": 200, "message": "删除成功"})

    @action(methods=['post'], detail=False)
    def update_group_apply(self, request):
        """
        更新申请物资数量信息
        """
        req = request.data
        apply_list = req.get("applyList")
        update_type = req.get("updateType")
        if isinstance(apply_list, list) and check_apply_update_param(update_type):
            update_apply_ids = []
            for update_apply in update_apply_ids:
                update_apply_ids.append(update_apply["id"])
            all_apply_id = GroupApply.objects.values_list("id", flat=True)
            if not set(update_apply_ids).issubset(set(all_apply_id)):
                raise BusinessException(StatusEnums.CART_UPDATE_ERROR2)
            all_applies = []
            for apply in apply_list:
                temp_apply = GroupApply.objects.get(id=apply["id"])
                temp_apply.num = int(apply["num"])
                if update_type == 'status':
                    temp_apply.status = 5
                temp_apply.update_time = datetime.now()
                all_applies.append(temp_apply)
            if update_type == 'status':
                GroupApply.objects.bulk_update(all_applies, ['status', 'update_time'])
            else:
                GroupApply.objects.bulk_update(all_applies, ['num', 'update_time'])
        else:
            raise BusinessException(StatusEnums.ADX_UPDATE_ERROR)
        return get_result({"code": 200, "message": "修改成功"})

    @action(methods=['get'], detail=False)
    def get_personal_goods(self, request):
        """
        获取个人物资
        """
        # 获取params
        req = request.GET
        username = request.user.username
        page_limit = int(request.GET.get('pageLimit', 10))
        page = int(request.GET.get('page', 1))
        id_list = request.GET.get('idList', None)
        personal_serializer = personalSerializer(data={
            "username": username
        })
        if not personal_serializer.is_valid():
            raise ValueError(get_error_message(personal_serializer))

        # 获得查询集
        queryset = GroupApply.objects.filter(username=username)

        unnecessary_goods = []  # 用于记录被过滤掉的物品
        # 获取form的内容
        # form = json.loads(form)
        name = req.get('name')
        code = req.get('code')
        location = req.get('city')
        status = req.get('status')
        good_type = req.get('type')

        personal_form_serializer = personalFormSerializer(data={
            "good_name": name,
            "good_code": code
        })

        if not personal_form_serializer.is_valid():
            raise ValueError(get_error_message(personal_serializer))

        # 建立初始查询条件query
        query = Q(status__gte=0)

        # 对form内容进行处理，获得所需查询集
        if name:
            goods = Good.objects.filter(good_name__icontains=name)
            good_codes = []
            for good in goods:
                good_codes.append(good.good_code)
            for item in queryset:
                if item.good_code not in good_codes:
                    unnecessary_goods.append(item.good_code)
        if code:
            query = query & Q(good_code=code)
        if location and location != '0':
            query = query & Q(position__icontains=location)
        if status and int(status) != 0:
            query = query & Q(status=status)
        queryset = queryset.filter(query)
        if good_type and int(good_type) != 0:
            goods = Good.objects.filter(good_type_id=good_type, status=1)
            good_codes = []
            for good in goods:
                good_codes.append(good.good_code)
            for item in queryset:
                if item.good_code not in good_codes:
                    unnecessary_goods.append(item.good_code)

        serializer_data = []

        # 序列化查询集
        if id_list:
            id_list = json.loads(id_list)
            for item in queryset:
                if item.good_code not in unnecessary_goods and item.id in id_list:
                    serializer_data.append(item.to_json())
        else:
            for item in queryset:
                if item.good_code not in unnecessary_goods:
                    serializer_data.append(item.to_json())

        # 自定义分页
        total = len(serializer_data)
        serializer_data = serializer_data[(page - 1) * page_limit:page * page_limit]
        serializer_data.append({'total': total})

        return JsonResponse(success_code(serializer_data))

    @action(methods=['GET'], detail=False)
    def get_good_status_list(self, request):
        """
        获取物资状态列表
        """
        good_status_list = []
        for item in GroupApply.STATUS_TYPE:
            good_status_list.append({'id': item[0], 'status_name': item[1]})
        return JsonResponse(success_code(good_status_list))

    @action(methods=['post'], detail=False)
    def confirm_receipt(self, request):
        "确认收货"
        body = request.data
        id_list = body.get('idList')
        serializer = ConfirmReceiptSerializer(data={"id_list": id_list})
        if not serializer.is_valid():  # 校验参数
            err_msg = get_error_message(serializer)
            return get_result({'result': False, 'message': err_msg})
        queryset = GroupApply.objects.filter(id__in=id_list, status=5)  # 获取查询集
        if len(queryset) != len(id_list):  # 列表id中存在状态为非待收货的物品
            raise BusinessException(StatusEnums.PARAMS_ERROR)
        with transaction.atomic():
            queryset.update(status=2)
        return JsonResponse(success_code({}))


class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializers

    @action(methods=['GET'], detail=False)
    def get_good_detail(self, request):
        """
          根据商品id获取商品详情信息
          """
        req_data = request.GET
        good_id = req_data.get("good_id", 0)
        # 校验参数
        if not check_param_id(good_id):
            raise BusinessException(StatusEnums. GOODID_ERROR)
        try:
            good = Good.objects.get(id=good_id, status=1).to_json()
        except Good.DoesNotExist:
            raise BusinessException(StatusEnums.NOTFOUND_ERROR)
        return JsonResponse(success_code(good))

    @action(methods=['get'], detail=False)
    def get_good_list(self, request):
        """
        获取商品列表
        """
        req_data = request.GET
        # 筛选项参数拼接查询条件
        query = Q(status=1)
        # 需要筛选的字段
        conditions = ('good_code', 'good_name')
        for condition in conditions:
            # 查询筛选值
            condition_value = req_data.get(condition, None)
            if check_param_str(condition_value):
                # 新建模糊查询筛选条件字典
                new_query = {condition + '__contains': condition_value}
                # 拼接筛选条件
                query = query & Q(**new_query)

        # 商品类型筛选条件
        good_type_id = req_data.get("good_type_id", 0)
        try:
            good_type_id = int(good_type_id)
            if good_type_id > 0:
                query = query & Q(good_type_id=good_type_id)
        except ValueError:
            raise BusinessException(StatusEnums.CART_TYPE_ERROR)
        # 获取指定页元素，获取当前页的商品 ！要不要try catch
        cur_goods, total_num = tool_paginator(req_data, Good, query, 'page', 'size')

        # 返回数据
        data = {"total_num": total_num,
                "good_list": [good.to_json() for good in cur_goods]}  # ！这里还是for循环内部查询了数据库
        return JsonResponse(success_code(data))

    @action(methods=['post'], detail=False)
    def add_good(self, request):
        """添加商品"""
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        good = request.data
        # 参数校验
        good_serializers = GoodSerializers(data=good)
        if not good_serializers.is_valid():
            message = get_error_message(good_serializers)
            return get_result({"code": 7100, "result": False, "message": message})  # 输出错误方式
        # 检查商品编码是否存在
        good_code = good_serializers.validated_data.get("good_code")
        if Good.objects.filter(good_code=good_code, status=1).exists():
            raise BusinessException(StatusEnums.INPUT_GOODS_ERROR)
        # 检验商品类型是否存在
        good_type_id = good_serializers.validated_data.get("good_type_id")
        if not GoodType.objects.filter(id=good_type_id).exists():
            raise BusinessException(StatusEnums.CARTTYPE_NULL_ERROR)
        with transaction.atomic():
            Good.objects.create(**good)
        return get_result({"message": "新增商品成功"})

    @action(methods=['post'], detail=False)
    def update_good(self, request):
        """修改商品信息"""
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        good = request.data
        # 参数校验
        good_serializers = GoodSerializers(data=good)
        if not good_serializers.is_valid():
            message = get_error_message(good_serializers)
            return get_result({"code": 1, "result": False, "message": message})
        # 校验id
        good_id = good.get("id", 0)
        if not check_param_id(good_id):
            raise BusinessException(StatusEnums.GOOD_ID_ERROR)
        # 校验商品是否存在
        if not Good.objects.filter(id=good_id, status=1).exists():
            raise BusinessException(StatusEnums.CART_NO_ERROR)
        # 检验商品编码是否重复(good_code相同，但id不同的商品)
        good_code = good_serializers.validated_data.get("good_code")
        if Good.objects.filter(Q(good_code=good_code) & ~Q(id=good_id) & Q(status=1)).exists():
            raise BusinessException(StatusEnums.INPUT_GOODS_ERROR)
        # 校验商品类型是否存在
        good_type_id = good_serializers.validated_data.get("good_type_id")
        if not GoodType.objects.filter(id=good_type_id).exists():
            raise BusinessException(StatusEnums.CARTTYPE_NULL_ERROR)
        # 更新数据
        Good.objects.filter(id=good_id).update(**good, update_time=datetime.now())
        return get_result({"message": "修改商品信息成功"})

    @action(methods=['post'], detail=False)
    def down_good(self, request):
        """商品下架"""
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        req = request.data
        good_id = req.get('id', 0)
        # 校验参数
        if not check_param_id(good_id):
            raise BusinessException(StatusEnums.GOODID_ERROR)
        # 校验商品是否存在
        if not Good.objects.filter(id=good_id, status=1).exists():
            raise BusinessException(StatusEnums.CART_NO_ERROR)
        Good.objects.filter(id=good_id).update(status=0)
        return get_result({"message": "下架商品成功"})

    @action(methods=['get'], detail=False)
    def get_good_code_list(self, request):
        """获取商品编码列表"""
        good_list = Good.objects.all()
        good_type_list = [good_item.good_code for good_item in good_list]
        return JsonResponse(success_code(good_type_list))


class GoodTypeViewSet(viewsets.ModelViewSet):
    queryset = GoodType.objects.all()
    serializer_class = GoodTypeSerializers

    @action(methods=['POST'], detail=False)
    def add_good_type(self, request):
        """新增商品类型"""
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if not flag:
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        req = request.data
        # 参数校验
        good_type_serializers = GoodTypeSerializers(data=req)
        if not good_type_serializers.is_valid():
            message = get_error_message(good_type_serializers)
            return get_result({"code": 7100, "result": False, "message": message})
        # 验证该商品类型是否存在
        type_name = good_type_serializers.validated_data.get("type_name")
        if GoodType.objects.filter(type_name=type_name).exists():
            raise BusinessException(StatusEnums.INPUT_TYPE_ERROR)
        good_type = GoodType.objects.create(type_name=type_name)
        return get_result({"message": "新增商品类型成功", "data": {"id": good_type.id}})

    @action(methods=['get'], detail=False)
    def get_good_type_list(self, request):
        """获取商品类别列表"""
        good_types = GoodType.objects.all()
        good_type_list = [good_type.to_json() for good_type in good_types]
        return JsonResponse(success_code(good_type_list))

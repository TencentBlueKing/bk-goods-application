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

from django.conf.urls import url
from django.urls import path

from ..tools import analysis_apply_excel
from . import views

urlpatterns = (
    url(r"^$", views.home),
    path("get_position_list", views.get_position_list),  # 获取地区列表
    path("analysis_apply_excel", analysis_apply_excel.analysis_apply_excel),  # 解析excel数据
    path("get_root_position_list", views.get_root_position_list),  # 获取一级地区列表
    path("get_sub_position_list", views.get_sub_position_list),  # 获取下一级地区列表
    path("get_leader", views.get_leader),  # 获取用户的组长
    path("submit_apply_list", views.submit_apply_list),  # 提交物资申请
    path("if_leader_or_secretary", views.if_leader_or_secretary),  # 是否是管理员（秘书）或组长
    path("get_apply_users", views.get_apply_users),  # 获取可管理的用户
    path("get_goods_apply", views.get_goods_apply),  # （筛选）获取需要需要审核的物资申请
    path("if_admin", views.if_admin),  # 判断是否秘书
    path("examine_apply", views.examine_apply)  # 审核申请
)

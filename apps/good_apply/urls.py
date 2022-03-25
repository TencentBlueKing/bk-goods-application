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
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..tools import analysis_apply_excel
from . import views

urlpatterns = [
    url(r"^$", views.home),
    path("analysis_apply_excel", analysis_apply_excel.analysis_apply_excel),  # 解析excel数据
    path("get_leader", views.get_leader),  # 获取用户的导员
    path("if_leader_or_secretary", views.if_leader_or_secretary),  # 是否是管理员（秘书）或导员
    path("get_apply_users", views.get_apply_users),  # 获取可管理的用户
]

router = DefaultRouter()
router.register(r'position', views.PositionViewSet, basename="position")
router.register(r'apply', views.ApplyViewSet, basename="apply")

urlpatterns += [
    path('', include(router.urls))
]

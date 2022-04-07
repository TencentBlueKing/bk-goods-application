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
    # url('test', views.test),
    path("analysis_apply_excel", analysis_apply_excel.analysis_apply_excel),  # 解析excel数据
]

router = DefaultRouter()
router.register(r'position', views.PositionViewSet, basename="position")
router.register(r'apply', views.ApplyViewSet, basename="apply")
router.register(r'organizationmember', views.OrganizationMemberViewSet, basename="organizationmember")
router.register(r'organization', views.OrganizationViewSet, basename="organization")
router.register(r'secretary', views.SecretaryViewSet, basename="secretary")
router.register(r'applytoorg', views.ApplyToOrgViewSet, basename="applytoorg")

urlpatterns += [
    path('', include(router.urls))
]

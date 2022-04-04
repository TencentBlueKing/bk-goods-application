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
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..tools import del_excel, derive_excel, import_cart_excel
from . import views

urlpatterns = [


    path("upload_img", views.upload_img),  # 上传图片
    path('del_pics', views.del_pics),  # 删除图片
    path("import_excel", import_cart_excel.import_cart_excel),  # 通过excel导入数据到部门所需物资
    path("derive_excel", derive_excel.derive_excel),  # 导出部门所需物资数据
    path("del_excel", del_excel.del_excel),  # 删除excel文件
]

router = DefaultRouter()
router.register(r'withdraw', views.WithdrawViewSet, basename="withdraw")
router.register(r'withdraw_reason', views.WithdrawReasonViewSet, basename="withdraw_reason")
router.register(r'user_info', views.UserViewSet, basename="user_info")
router.register(r'cart', views.CartViewSet, basename="cart")
router.register(r'group_apply', views.GroupApplyViewSet, basename="group_apply")
router.register(r'good', views.GoodViewSet, basename="goods")
router.register(r'goodtype', views.GoodTypeViewSet, basename='goodtype')

urlpatterns += [
    path('', include(router.urls))
]

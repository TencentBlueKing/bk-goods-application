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

from apps.tools import derive_excel, del_excel, import_excel

from . import views

urlpatterns = (
    path("get_good_detail", views.get_good_detail),  # 商品详情
    url(r"^get_personal_goods/$", views.get_personal_goods),  # 获取个人物资接口
    path("get_good_list", views.get_good_list),  # 获取商品列表
    path("get_good_type_list", views.get_good_type_list),  # 获取商品类别列表
    path("get_good_status_list", views.get_good_status_list), # 获取物资状态列表
    path("derive_excel", derive_excel.derive_excel),  # 导出excel
    path("del_excel", del_excel.del_excel),  # 删除excel文件
    path("add_good", views.add_good),  # 新增商品信息
    path("update_good", views.update_good),  # 修改商品信息
    path("add_good_type", views.add_good_type),  # 新增商品类型信息
    path("down_good", views.down_good),  # 下架商品
    path("upload_img", views.upload_img),  # 上传图片
    path("import_excel", import_excel.import_excel),  # 通过excel导入数据到部门所需物资
    path("get_withdraw_reason", views.get_withdraw_reason),  # 获取所有退回商品原因
    path("add_withdraw_apply", views.add_withdraw_apply),  # 提交退回商品申请
)

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

from . import views

urlpatterns = (
    path("get_good_detail", views.get_good_detail),  # 商品详情
    url(r"^goods/$", views.get_goods),  # 获取指定商品信息
    url(r"^types/$", views.get_types),  # 获取商品类型
    path("get_shopping_car", views.get_shopping_cart),  # 获取购物车信息
    path("delete_cart_goods", views.delete_cart_goods),  # 删除购物车信息
    path("update_cart_goods", views.update_cart_goods),  # 修改购物车数量信息
    path("update_group_apply", views.update_group_apply),   # 给申请表添加数据
    path("add_cart_goods", views.add_cart_goods), # 添加物资到购物车/更新购物车物资数量
    path("get_good_list", views.get_good_list),  # 获取商品列表
    path("get_good_type_list", views.get_good_type_list),  # 获取商品类别列表
    path("add_good", views.add_good),  # 新增商品信息
    path("update_good", views.update_good),  # 修改商品信息
    path("add_good_type", views.add_good_type),  # 新增商品类型信息
    path("down_good", views.down_good),  # 下架商品
    path("upload_img", views.upload_img),  # 上传图片
)

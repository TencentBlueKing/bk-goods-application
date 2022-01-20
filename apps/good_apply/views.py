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

from django.shortcuts import render
from django.views.decorators.http import require_GET

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
from apps.good_apply.models import Position, Secretary
from apps.tools.response import get_result


def home(request):
    """
    首页
    """
    return render(request, "index.html")

@require_GET
def get_position_list(request):
    positions = Position.objects.all()
    position_list = [position.to_json() for position in positions]
    return get_result({"data": position_list})

@require_GET
def if_admin(request):
    ifAdmin = False
    username = request.GET.get('username', None)
    if username:
        if Secretary.objects.filter(username=username).first():
            ifAdmin = True
    return get_result({"result": ifAdmin})

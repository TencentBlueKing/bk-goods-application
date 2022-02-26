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

# Register your models here.
from apps.good_apply.models import Apply, Position, Secretary
from apps.good_purchase.models import (Cart, Good, GoodType, GroupApply,
                                       UserInfo, Withdraw, WithdrawReason)
from django.contrib import admin


class GoodTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['type_name']}),
    ]
    list_display = ('type_name',)
    search_fields = ['type_name']


class GoodAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['good_code']}),
        (None, {'fields': ['good_name']}),
        (None, {'fields': ['good_type_id']}),
        (None, {'fields': ['price']}),
        (None, {'fields': ['pics']}),
        (None, {'fields': ['introduce']}),
        (None, {'fields': ['remark']}),
        (None, {'fields': ['specifications']}),
        (None, {'fields': ['status']}),
    ]
    list_display = ('good_name',)
    search_fields = ['good_name']
    list_filter = ['good_type_id']


class CartAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        (None, {'fields': ['good_id']}),
        (None, {'fields': ['num']}),
    ]
    list_display = ('username',)
    search_fields = ['username']
    list_filter = ['username']


class GroupApplyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['good_code']}),
        (None, {'fields': ['num']}),
        (None, {'fields': ['username']}),
        (None, {'fields': ['position']}),
        (None, {'fields': ['phone']}),
        (None, {'fields': ['status']}),
        (None, {'fields': ['remarks']}),
    ]
    list_display = ('good_code', 'username')
    search_fields = ['username', 'good_code']
    list_filter = ['position', 'username']


class WithdrawAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['good_apply_id']}),
        (None, {'fields': ['username']}),
        (None, {'fields': ['reason_id']}),
        (None, {'fields': ['position']}),
        (None, {'fields': ['status']}),
        (None, {'fields': ['remarks']}),
    ]
    list_display = ('good_apply_id', 'username')
    search_fields = ['username', 'good_code']
    list_filter = ['position', 'username']


class WithdrawReasonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['reason_type']}),
    ]
    list_display = ('reason_type',)
    search_fields = ['reason_type']


class UserInfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        (None, {'fields': ['phone']}),
        (None, {'fields': ['position']}),
    ]
    list_display = ('username',)
    list_filter = ['position']
    search_fields = ['username']


class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['position_code']}),
        (None, {'fields': ['name']}),
        (None, {'fields': ['parent_code']}),
    ]
    list_display = ('name',)
    list_filter = ['parent_code']
    search_fields = ['name']


class SecretaryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
    ]
    list_display = ('username',)
    search_fields = ['username']


class ApplyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['good_code']}),
        (None, {'fields': ['good_name']}),
        (None, {'fields': ['num']}),
        (None, {'fields': ['require_date']}),
        (None, {'fields': ['reason']}),
        (None, {'fields': ['position']}),
        (None, {'fields': ['status']}),
        (None, {'fields': ['apply_user']}),
    ]
    list_display = ('good_name',)
    list_filter = ['status', 'position', 'apply_user']
    search_fields = ['good_name', 'apply_user']


admin.site.register(GoodType, GoodTypeAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(GroupApply, GroupApplyAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(WithdrawReason, WithdrawReasonAdmin)
admin.site.register(Secretary, SecretaryAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Apply, ApplyAdmin)

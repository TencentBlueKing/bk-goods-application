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

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, platforms
from celery.schedules import crontab
from django.conf import settings

# http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#running-the-worker-with-superuser-privileges-root
# for root start celery

platforms.C_FORCE_ROOT = True

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery("proj", broker='redis://localhost:6379/0', backend='redis://localhost')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# 设置定时任务
app.conf.beat_schedule = {
    # 设置定时任务的参数,key可以自定义,见名知义,value为定时任务的相关参数的字典
    'add_member_from_bk_usermanagement': {
        # 指定要执行的任务函数
        'task': 'apps.good_apply.tasks.add_member_from_bk_usermanagement',
        # 设置定时启动的频率,每天两点执行一次任务函数
        'schedule': crontab(minute="0", hour="2"),
        # 传入任务函数的参数,可以是一个列表或元组,如果函数没参数则为空列表或空元组
        'args': [settings.INNERLIST]
    }
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {!r}".format(self.request))

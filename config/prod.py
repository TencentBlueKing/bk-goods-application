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

from config import RUN_VER

if RUN_VER == "open":
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = "PRODUCT"
# # APP本地静态资源目录
# STATIC_URL = "static/"
# 前端静态url
BK_STATIC_URL = STATIC_URL + "dist"
BK_APPLY_STATIC_URL = STATIC_URL + "apply_dist"

# 只对正式环境日志级别进行配置，可以在这里修改
# from blueapps.conf.log import set_log_level # noqa
# LOG_LEVEL = "ERROR"
# LOGGING = set_log_level(locals())

# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_NAME'),
            'USER': os.environ.get('MYSQL_USER'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
            'HOST': os.environ.get('MYSQL_HOST'),
            'PORT': os.environ.get('MYSQL_PORT'),
        }
    }
)

MEDIA_URL = '%smedia/' % SITE_URL
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

# 设置为 celery 后端消息队列
BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(
    user=RABBITMQ_USER,
    password=RABBITMQ_PASSWORD,
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    vhost=RABBITMQ_VHOST,
)

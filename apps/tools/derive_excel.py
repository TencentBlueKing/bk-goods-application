import datetime
import json
import os

from django.views.decorators.http import require_POST
import xlwt

from apps.good_apply.models import Apply
from apps.good_purchase.models import Good, Cart, GoodType, GroupApply
from apps.tools.response import get_result
from django.conf import settings

from apps.utils.deriveClass import DeriveModel
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException


@require_POST
def derive_excel(request):
    """
    导出excel表
    """
    body = request.body
    body = json.loads(body)
    model = body.get('model')
    goods = body.get('dataList')
    username = request.user.__str__()

    if not model or not goods or not username:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    derive = DeriveModel(model, goods, username)
    derive.run()

    return get_result(derive.result)

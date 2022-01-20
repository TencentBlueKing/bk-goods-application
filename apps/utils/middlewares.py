import json
import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from apps.utils.exceptions import BusinessException
from apps.utils.response import ExceptResponse

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()


class take_params(object):  # 定义类方便传参
    def __init__(self):
        self.errmsg = ''

    def set_errmsg(self, errmsg):
        self.errmsg = errmsg


class ViewErrorMiddleware(MiddlewareMixin, take_params):

    def process_exception(self, request, exception):  # 处理异常
        if isinstance(exception, BusinessException):  # 若是自定义类
            data = ExceptResponse(exception.enum_cls).data()  # 序列化数据
            logger.error(data['message'], exc_info=True)  # 打印错误日志
            return JsonResponse(data)
        else:  # 若不是自定义类
            errmsg = exception.__str__()  # 拿到非自定义类错误信息
            self.set_errmsg(errmsg)

    def process_response(self, request, response):
        if response.status_code >= 400:  # 若为异常响应
            result = {
                "code": response.status_code,
                "result": False,
                "message": self.errmsg,
                "data": {}
            }
            return JsonResponse(result, status=response.status_code)
        return response
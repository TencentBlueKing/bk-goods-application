import re

from apps.good_purchase.models import Good, GoodType, GroupApply, UserInfo
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from rest_framework import serializers


class GoodSerializers(serializers.Serializer):
    good_code = serializers.CharField(max_length=30, required=True,
                                      error_messages={'max_length': '商品编码过长',
                                                      'required': '商品编码不可为空',
                                                      'blank': '商品编码不可为空'}
                                      )
    good_name = serializers.CharField(max_length=50, required=True,
                                      error_messages={'max_length': '商品名称过长',
                                                      'required': '商品名称不可为空',
                                                      'blank': '商品名称不可为空'})
    good_type_id = serializers.IntegerField(required=True, error_messages={'required': '商品类型编号不可为空',
                                                                           'invalid': '商品类别id不是合法数字'})
    price = serializers.DecimalField(max_digits=24, decimal_places=2,
                                     error_messages={'required': '商品价格不可为空',
                                                     'invalid': '商品价格不是合法数字'})
    pics = serializers.CharField(required=True, error_messages={'required': '商品参考图不可为空',
                                                                'blank': '商品参考图不可为空'})
    introduce = serializers.CharField(allow_blank=True)
    remark = serializers.CharField(allow_blank=True)
    specifications = serializers.CharField(allow_blank=True)

    class Meta:
        # 设置使用的模型
        model = Good


class GoodTypeSerializers(serializers.Serializer):
    type_name = serializers.CharField(max_length=20, required=True,
                                      error_messages={
                                          'max_length': '类型名称为空',
                                          'required': '类型名称不可为空',
                                          'blank': '类型名称不可为空'
                                      })

    class Meta:
        model = GoodType


class CheckWithdrawsSeralizers(serializers.Serializer):
    good_ids = serializers.ListField(required=True,
                                     error_messages={'required': '个人物资id列表不可为空',
                                                     'invalid': '物资id列表参数不合法'},
                                     child=serializers.IntegerField(min_value=1,
                                                                    error_messages={'min_value': '个人物资存在不合法id',
                                                                                    'invalid': '物资id类型不合法'}),
                                     )
    reason_id = serializers.IntegerField(required=True, min_value=1, error_messages={
        'min_value': '退货原因id不合法', 'required': '退回原因id不可为空', 'invalid': '退回原因id不是合法数字'})
    province = serializers.CharField(required=True, max_length=100,
                                     error_messages={'max_length': '退货省份地址参数过长',
                                                     'required': '退货省份地址不可为空',
                                                     'blank': '退货省份地址不可为空'})
    city = serializers.CharField(required=True, max_length=100,
                                 error_messages={'max_length': '退货城市地址参数过长'})
    remark = serializers.CharField(allow_blank=True)


class GroupApplySerializers(serializers.Serializer):
    good_code = serializers.CharField(max_length=30, required=True,
                                      error_messages={'max_length': '商品编码过长',
                                                      'required': '商品编码不可为空',
                                                      'blank': '商品编码不可为空'}
                                      )
    username = serializers.CharField(max_length=30, required=True,
                                     error_messages={'max_length': '用户名过长',
                                                     'required': '用户名不可为空',
                                                     'blank': '用户名不可为空'})
    position = serializers.CharField(max_length=100, required=True,
                                     error_messages={'max_length': '地区名过长',
                                                     'required': '地区名不可为空',
                                                     'blank': '地区名不可为空'})
    num = serializers.IntegerField()

    def validate_good_code(self, value):
        if not Good.objects.filter(good_code=value, status=1).exists():
            raise BusinessException(StatusEnums.NOTFOUND_ERROR)
        else:
            return value

    def validate_username(self, value):
        if not UserInfo.objects.filter(username=value).exists():
            raise BusinessException(StatusEnums.USERNAME_NOT_EXIST_ERROR)
        else:
            return value

    def validate_num(self, value):
        if (not isinstance(value, int) and not isinstance(value, float)) or not value >= 0:
            raise BusinessException(StatusEnums.NUM_ERROR)
        else:
            return value

    class Meta:
        model = GroupApply


class personalSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True,
                                     error_messages={'max_length': '用户名过长',
                                                     'required': '用户名不可为空',
                                                     'blank': '用户名不可为空'})


class personalFormSerializer(serializers.Serializer):
    good_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True,
                                      required=False, error_messages={'max_length': '商品名过长'})
    good_code = serializers.CharField(max_length=30, allow_null=True, allow_blank=True,
                                      required=False, error_messages={'max_length': '商品编码过长'})


class delExcelSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        if not UserInfo.objects.filter(username=value).exists():
            raise BusinessException(StatusEnums.USERNAME_NOT_EXIST_ERROR)
        else:
            return value


class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True,
                                     error_messages={'max_length': '用户名过长',
                                                     'required': '必须传入用户名',
                                                     'blank': '用户名不可为空'})
    phone = serializers.CharField(max_length=30, allow_null=True, allow_blank=True,
                                  error_messages={'max_length': '号码过长'})
    position = serializers.CharField(max_length=30, allow_null=True, allow_blank=True,
                                     error_messages={'max_length': '地区名过长'})

    def validate_phone(self, value):
        if value:
            if not re.match(r"^1[35678]\d{9}$", value):
                raise BusinessException(StatusEnums.PHONE_ERROR)
        return value


class ConfirmReceiptSerializer(serializers.Serializer):
    id_list = serializers.ListField(required=True,
                                    error_messages={'required': '个人物资id列表不可为空',
                                                    'invalid': '物资id列表参数不合法'},
                                    child=serializers.IntegerField(min_value=1,
                                                                   error_messages={'min_value': '个人物资存在不合法id',
                                                                                   'invalid': '物资id类型不合法'}),
                                    )

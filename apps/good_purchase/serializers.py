from apps.good_purchase.models import Good, GoodType
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
    pics = serializers.CharField(allow_blank=True)
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
    position = serializers.CharField(required=True, max_length=100,
                                     error_messages={'max_length': '退货地址参数过长',
                                                     'required': '退货地址不可为空',
                                                     'blank': '退货地址不可为空'})
    remark = serializers.CharField(allow_blank=True)

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

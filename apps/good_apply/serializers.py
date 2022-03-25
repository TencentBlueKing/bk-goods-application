import datetime

from apps.good_apply.models import Apply, Position
from rest_framework import serializers


class PreApplySerializers(serializers.Serializer):
    good_code = serializers.CharField(max_length=30, required=True,
                                      error_messages={'max_length': '物品编码过长',
                                                      'required': '物品编码不可为空',
                                                      'blank': '物品编码不可为空'})
    good_name = serializers.CharField(max_length=50, required=True,
                                      error_messages={'max_length': '物品名称过长',
                                                      'required': '物品名称不可为空',
                                                      'blank': '物品名称不可为空'})
    num = serializers.IntegerField(required=True, min_value=1, error_messages={'min_value': '申请最少数量为1',
                                                                               'required': '申请数量不可为空',
                                                                               'invalid': '申请数量不是合法数字'})
    require_date = serializers.DateField(default=datetime.datetime.now() + datetime.timedelta(days=7),
                                         error_messages={'invalid': '期望领用日期不合法'})
    # 申请人
    apply_user = serializers.CharField(max_length=30, required=True,
                                       error_messages={'max_length': '申请人username过长',
                                                       'required': '申请人不可为空',
                                                       'blank': '申请人不可为空'})


class ApplyCheckSerializers(serializers.Serializer):
    good_code = serializers.CharField(max_length=30, required=True,
                                      error_messages={'max_length': '物品编码过长',
                                                      'required': '物品编码不可为空',
                                                      'blank': '物品编码不可为空'})
    good_name = serializers.CharField(max_length=50, required=True,
                                      error_messages={'max_length': '物品名称过长',
                                                      'required': '物品名称不可为空',
                                                      'blank': '物品名称不可为空'})
    num = serializers.IntegerField(required=True, min_value=1, error_messages={'min_value': '申请最少数量为1',
                                                                               'required': '申请数量不可为空',
                                                                               'invalid': '申请数量不是合法数字'})
    require_date = serializers.DateField(default=datetime.datetime.now() + datetime.timedelta(days=7),
                                         error_messages={'invalid': '期望领用日期不合法'})
    reason = serializers.CharField(max_length=255, required=True,
                                   error_messages={'max_length': '申请原因过长',
                                                   'required': '申请原因不可为空',
                                                   'blank': '申请原因不可为空'})   # 每一个都要写申请原因？
    # 校区
    school = serializers.CharField(max_length=30, required=True,
                                   error_messages={'max_length': '校区地址过长',
                                                   'required': '校区地址不可为空',
                                                   'blank': '校区地址不可为空'})
    # 校区
    academy = serializers.CharField(max_length=50, required=True,
                                    error_messages={'max_length': '学院地址过长',
                                                    'required': '学院地址不可为空',
                                                    'blank': '学院地址不可为空'})
    # 详细地址
    detail_position = serializers.CharField(max_length=70, required=True,
                                            error_messages={'max_length': '详细地址过长',
                                                            'required': '详细地址不可为空',
                                                            'blank': '详细地址不可为空'})
    # 申请人
    apply_user = serializers.CharField(max_length=30, required=True,
                                       error_messages={'max_length': '申请人username过长',
                                                       'required': '申请人不可为空',
                                                       'blank': '申请人不可为空'})

    def validate_require_date(self, require_date):
        today = datetime.date.today()
        if require_date >= today:
            return require_date
        else:
            raise ValueError('期望领用日期不能为今天以前的日期')


class ApplySerializers(serializers.ModelSerializer):
    apply_time = serializers.DateTimeField(source='create_time')
    status = serializers.CharField(max_length=120, source='get_status_display')

    class Meta:
        model = Apply
        fields = ['id', 'good_code', 'good_name', 'num', 'require_date', 'reason', 'position', 'status',
                  'apply_user', 'apply_time']


class ApplyPostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = ['id', 'good_code', 'good_name', 'num', 'reason']


class IDListSeralizers(serializers.Serializer):
    apply_id_list = serializers.ListField(required=True,
                                          error_messages={'required': '个人物资id列表不可为空',
                                                          'invalid': '物资id列表参数不合法'},
                                          child=serializers.IntegerField(min_value=1,
                                                                         error_messages={'min_value': '个人物资存在不合法id',
                                                                                         'invalid': '物资id类型不合法'}),
                                          )


class PositionSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=20, source='position_code')

    class Meta:
        model = Position
        fields = ['id', 'code', 'name']

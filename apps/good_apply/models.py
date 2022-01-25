from django.db import models

# Create your models here.


# 时间抽象表
class TimeBasic(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        abstract = True


# 秘书
class Secretary(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="秘书用户名")

    class Meta:
        verbose_name = "秘书表"
        verbose_name_plural = "秘书表"


# 地区
class Position(models.Model):
    position_code = models.CharField(max_length=10, unique=True, verbose_name="地区代码")
    name = models.CharField(max_length=20, verbose_name="地区名")
    parent_code = models.CharField(max_length=10, null=True, verbose_name="上级地区代码")

    class Meta:
        verbose_name = "地区表"
        verbose_name_plural = "地区表"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


# 申请表
class Apply(TimeBasic):
    STATUS_TYPE = (
        (0, "申请终止"),
        (1, "组长审核中"),
        (2, "管理员审核中"),
        (3, "审核完成")
    )
    good_code = models.CharField(max_length=30, verbose_name="物资编号")
    good_name = models.CharField(max_length=50, verbose_name="物资名称")
    num = models.IntegerField(verbose_name="申请数量")
    require_date = models.DateField(verbose_name="期望领用日期")
    reason = models.CharField(max_length=255, verbose_name="申请原因")
    position = models.CharField(max_length=100, verbose_name="所在地区")
    status = models.IntegerField(default=1, choices=STATUS_TYPE, verbose_name="申请状态")
    apply_user = models.CharField(max_length=30, verbose_name="申请人")

    class Meta:
        verbose_name = "申请表"
        verbose_name_plural = "申请表"

    def to_json(self):
        return {
            "id": self.id,
            "good_code": self.good_code,
            "good_name": self.good_name,
            "num": self.num,
            "require_date": self.require_date,
            "reason": self.reason,
            "position": self.position,
            "status": self.get_status_display(),
            "apply_user": self.apply_user
        }


# 申请审核表
class Review(TimeBasic):
    IDENTITY_TYPES = (
        (1, '组长'),
        (2, '秘书')
    )
    RESULT_TYPES = (
        (1, '通过'),
        (2, '未通过')
    )
    apply_id = models.IntegerField(verbose_name="申请物资id")
    reviewer = models.CharField(max_length=30, verbose_name="审核人")
    reviewer_identity = models.IntegerField(verbose_name="审核人身份", choices=IDENTITY_TYPES)
    result = models.IntegerField(verbose_name="审核结果", choices=RESULT_TYPES)
    reason = models.CharField(max_length=255, verbose_name="审核意见")

    class Meta:
        verbose_name = "申请审核表"
        verbose_name_plural = "申请审核表"

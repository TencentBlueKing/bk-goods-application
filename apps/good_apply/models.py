from apps.abstract_models.TimeBasic import TimeBasic
from django.db import models

# Create your models here.


# 秘书
class Secretary(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="秘书用户名")
    org_id = models.BigIntegerField(verbose_name="组id", null=True, blank=True)

    class Meta:
        verbose_name = "秘书表"
        verbose_name_plural = "秘书表"


# 地区
class Position(models.Model):
    position_code = models.CharField(max_length=10, unique=True, verbose_name="地区代码")
    name = models.CharField(max_length=20, verbose_name="地区名")
    parent_code = models.CharField(max_length=10, null=True, verbose_name="上级地区代码")
    org_id = models.BigIntegerField(verbose_name="组id", null=True, blank=True)

    class Meta:
        verbose_name = "地区表"
        verbose_name_plural = "地区表"

    def to_json(self):
        return {
            "id": self.id,
            "code": self.position_code,
            "name": self.name
        }


# 申请表
class Apply(TimeBasic):
    STATUS_TYPE = (
        (0, "申请终止"),
        (1, "管理员审核中"),
        (2, "审核完成")
    )
    good_code = models.CharField(max_length=30, verbose_name="物资编号")
    good_name = models.CharField(max_length=50, verbose_name="物资名称")
    num = models.IntegerField(verbose_name="申请数量")
    require_date = models.DateField(verbose_name="期望领用日期")
    reason = models.CharField(max_length=255, verbose_name="申请原因")
    position = models.CharField(max_length=100, verbose_name="所在地区")
    status = models.IntegerField(default=1, choices=STATUS_TYPE, verbose_name="申请状态")
    apply_user = models.CharField(max_length=30, verbose_name="申请人")
    org_id = models.BigIntegerField(verbose_name="组id", null=True, blank=True)

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
            "apply_user": self.apply_user,
            "apply_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }


# 申请审核表
class Review(TimeBasic):
    IDENTITY_TYPES = (
        (1, '管理员'),
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
    org_id = models.BigIntegerField(verbose_name="组id", null=True, blank=True)

    class Meta:
        verbose_name = "申请审核表"
        verbose_name_plural = "申请审核表"

# 组表


class Organization(models.Model):
    id = models.BigAutoField(verbose_name="组id", primary_key=True)
    group_name = models.CharField(max_length=20, verbose_name="组名")

    class Meta:
        verbose_name = "组表"
        verbose_name_plural = "组表"

    def to_json(self):
        return {
            "id": self.id,
            "group_name": self.group_name
        }


class OrganizationMember(models.Model):
    username = models.CharField(max_length=255, verbose_name="用户名")
    org_id = models.BigIntegerField(verbose_name="组id", null=True, blank=True)

    class Meta:
        verbose_name = "组成员表"
        verbose_name_plural = "组成员表"

    def to_json(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "org_id": self.org_id
        }


class ApplyToOrg(TimeBasic):
    STATUS_TYPE = (
        (1, '审核中'),
        (2, '同意加入'),
        (3, '拒绝加入')
    )

    apply_group_id = models.BigIntegerField(verbose_name='申请加入组id')
    status = models.IntegerField(verbose_name='申请状态', choices=STATUS_TYPE)

    class Meta:
        verbose_name = "申请加入组表"
        verbose_name_plural = "申请加入组表"

    def to_json(self):
        return {
            "id": self.id,
            "apply_group_id": self.apply_group_id,
            "username": self.create_user,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "status": self.get_status_display(),
        }

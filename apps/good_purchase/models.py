from django.db import models

# Create your models here.


# 时间抽象表
class TimeBasic(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        abstract = True


# 商品类型表
class GoodType(models.Model):
    type_name = models.CharField(max_length=20, unique=True, verbose_name="类型名称")

    class Meta:
        verbose_name = "商品类型表"

    def __str__(self):
        return self.type_name

    def to_json(self):
        return {
            "id": self.id,
            "type_name": self.type_name
        }


# 商品表
class Good(TimeBasic):
    STATUS_TYPE = (
        (0, "已下架"),
        (1, "正常")
    )
    good_code = models.CharField(max_length=30, unique=True, verbose_name="物资编码")
    good_name = models.CharField(max_length=50, verbose_name="物资名称")
    good_type_id = models.IntegerField(verbose_name="物资类型")
    price = models.DecimalField(max_digits=24, decimal_places=2, verbose_name="参考价值")
    pics = models.TextField(verbose_name="商品图片")
    introduce = models.TextField(verbose_name="商品介绍")
    remark = models.CharField(max_length=255, verbose_name="商品备注")
    specifications = models.TextField(verbose_name="规格参数")
    status = models.BooleanField(default=1, choices=STATUS_TYPE, verbose_name="商品状态")

    class Meta:
        verbose_name = "商品表",
        ordering = ["-update_time"]

    def __str__(self):
        return self.good_name

    def to_json(self) -> dict:
        good_type_name = GoodType.objects.get(id=self.good_type_id).type_name
        return {
            "id": self.id,
            "good_code": self.good_code,
            "good_name": self.good_name,
            "good_type_id": self.good_type_id,
            "good_tye_name": good_type_name,
            "price": self.price,
            "pics": self.pics.split(";"),
            "introduce": self.introduce,
            "remark": self.remark,
            "specifications": self.specifications,
        }


# 个人信息表
class UserInfo(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="用户名")
    position = models.CharField(max_length=100, verbose_name="所在地区")
    phone = models.CharField(max_length=30, verbose_name="联系电话")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "position": self.position,
            "phone": self.phone
        }

# 购物车表
class Cart(TimeBasic):
    username = models.CharField(max_length=30, verbose_name="用户名")
    good_id = models.IntegerField(verbose_name="商品id")
    num = models.IntegerField(verbose_name="数量")

    def to_json(self) -> dict:
        res_good = Good.objects.get(id=self.good_id, status=1)
        good_name = res_good.good_name
        good_code = res_good.good_code
        good_type_id = res_good.good_type_id
        status = res_good.status
        price = res_good.price
        good_type_name = GoodType.objects.get(id=good_type_id).type_name
        return {
            "id": self.id,
            "good_code": good_code,
            "good_name": good_name,
            "good_type_id": good_type_id,
            "good_type_name": good_type_name,
            "price": price,
            "num": self.num,
            "status": status
        }

# 部门所需物资表
class GroupApply(TimeBasic):
    STATUS_TYPE = (
        (1, "已退回"),
        (2, "在使用"),
        (3, "退回中"),
        (4, "购买中")
    )
    good_code = models.CharField(max_length=30, verbose_name="商品编码")
    num = models.IntegerField(verbose_name="商品数量")
    username = models.CharField(max_length=30, verbose_name="使用人")
    position = models.CharField(max_length=100, verbose_name="所在地区")
    phone = models.CharField(max_length=30, verbose_name="联系电话")
    status = models.IntegerField(choices=STATUS_TYPE, verbose_name="物资状态")
    remarks = models.CharField(max_length=255, verbose_name="备注")

    def to_json(self) -> dict:
        good_name = Good.objects.get(good_code=self.good_code).good_name
        return {
            "id": self.id,
            "good_code": self.good_code,
            "num": self.num,
            "username": self.username,
            "position": self.position,
            "status": self.get_status_display(),
            "phone": self.phone,
            "good_name": good_name
        }

# 物资退回表
class Withdraw(TimeBasic):
    good_apply_id = models.IntegerField(verbose_name="物资id")
    username = models.CharField(max_length=30, verbose_name="申请人")
    reason_id = models.IntegerField(verbose_name="退回原因id")
    position = models.CharField(max_length=100, verbose_name="退库地址")
    remark = models.CharField(max_length=255, verbose_name="备注")
    status = models.BooleanField(default=0, verbose_name="退库状态")


# 退库原因表
class WithdrawReason(models.Model):
    reason_type = models.CharField(max_length=20, verbose_name="退货原因")

    def to_json(self):
        return {
            "id": self.id,
            "reason_name": self.reason_type
        }
from apps.good_purchase.models import Good, GoodType
from blueapps.account.models import User
from django.test import RequestFactory


def test_tool_good(self):

    self.goodtype_obj = GoodType.objects.create(id=1, type_name="办公用品")
    self.good_obj = Good.objects.create(id=1, good_code="ASN-123", good_name="桌子", good_type_id=1,
                                        price=3.6,
                                        pics="https://test/1.png",
                                        introduce="test", remark="test2", specifications="test3")


def test_tool_user(self):
    self.user = User.objects.create_superuser(username="admin", password="123456")
    self.request = RequestFactory()

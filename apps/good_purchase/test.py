import json

from apps.good_purchase.models import (Cart, Good, GoodType, GroupApply,
                                       UserInfo, Withdraw, WithdrawReason)
from apps.good_purchase.views import (CartViewSet, GoodTypeViewSet,
                                      GoodViewSet, GroupApplyViewSet,
                                      UserInfoViewSet, WithdrawReasonViewSet,
                                      WithdrawViewSet)
from blueapps.account.models import User
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

TEST_MIDDLEWARE = (
    "blueapps.utils.request_provider.RequestProvider",
)


class DjangoWebModelTest(TestCase):
    """"测试模型"""

    def setUp(self):
        UserInfo.objects.create(id=2, username="promise", phone="18729867137", position="西安市")
        GoodType.objects.create(id=3, type_name="生活用品")
        Good.objects.create(good_code="ASN-111", good_name="桌子", good_type_id=9, price="10",
                            pics="https://gitee.com/mypassion/fileimage/blob/master/images/1.png", introduce="好用",
                            remark="制作好", specifications="10cm", status=1)
        Cart.objects.create(username="3190911048X", good_id=3, num=6)
        GroupApply.objects.create(good_code="ASN-111", num=7, username="小许", position="延安市", phone="15029747733",
                                  status=4, remarks="尽快安排")
        Withdraw.objects.create(good_apply_id=1, username="promise", reason_id=1,
                                position="深圳市", remark="尽快退回", status=0)
        WithdrawReason.objects.create(reason_type="业务调整")

    def test_userinfo_model(self):
        """测试用户表"""
        result = UserInfo.objects.get(username="promise")
        self.assertEqual(result.phone, '18729867137')
        self.assertEqual(result.position, '西安市')

    def test_goodtype_model(self):
        """商品类型测试表"""
        result = GoodType.objects.get(id=3)
        self.assertEqual(result.type_name, "生活用品")

    def test_good_model(self):
        """商品测试表"""
        result = Good.objects.get(good_code="ASN-111")
        self.assertEqual(result.introduce, "好用")

    def test_cart_model(self):
        """购物车测试表"""
        result = Cart.objects.get(good_id=3)
        self.assertEqual(result.num, 6)

    def test_groupapply_model(self):
        """部门所需物资测试表"""
        result = GroupApply.objects.get(good_code="ASN-111")
        self.assertEqual(result.phone, "15029747733")
        self.assertEqual(result.position, "延安市")
        self.assertEqual(result.username, "小许")
        self.assertEqual(result.status, 4)
        self.assertEqual(result.num, 7)
        self.assertEqual(result.remarks, "尽快安排")

    def test_withdraw_model(self):
        """物资退回测试表"""
        result = Withdraw.objects.get(good_apply_id=1)
        self.assertEqual(result.username, "promise")
        self.assertEqual(result.reason_id, 1)
        self.assertEqual(result.position, "深圳市")
        self.assertEqual(result.remark, "尽快退回")
        self.assertEqual(result.status, 0)

    def test_withdrawreason_model(self):
        """退回原因申请表"""
        result = WithdrawReason.objects.get(reason_type="业务调整")
        self.assertEqual(result.reason_type, "业务调整")


class UserInfoModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.list_url = '/user_info/'
        self.request = RequestFactory()
        self.edit_user_info_url = '/user_info/edit_user_info/'
    #

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_list_api(self):
        request = self.request.get(self.list_url, data={})
        request.user = self.user
        response = UserInfoViewSet().list(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_edit_user_info_api(self):
        request = self.request.post(path=self.edit_user_info_url, data={
            "phone": "13772886398",
            "position": "深圳市"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = UserInfoViewSet().edit_user_info(request)
        self.assertEqual(response.status_code, 200)


class GoodTypeModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = GoodType.objects.create(type_name="办公用品")
        self.add_good_type_url = '/goodtype/add_good_type/'
        self.get_good_type_list_url = '/goodtype/get_good_type_list/'
        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_add_good_type_api(self):
        request = self.request.post(self.add_good_type_url, data={
            "type_name": "生活用品"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GoodTypeViewSet().add_good_type(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_good_type_list_api(self):
        request = self.request.get(self.get_good_type_list_url, data={})
        request.user = self.user
        response = GoodTypeViewSet().get_good_type_list(request)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)


class GoodModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.goodtype_obj = GoodType.objects.create(type_name="办公用品")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = Good.objects.create(good_code="ASN-123", good_name="桌子", good_type_id=1,
                                            price=3.6,
                                            pics="https://gitee.com/mypassion/fileimage/raw/master/images/1.png",
                                            introduce="test", remark="test2", specifications="test3")
        self.get_good_detail_url = '/good/get_good_detail/'
        self.get_good_list_url = '/good/get_good_list/'
        self.add_good_url = '/good/add_good/'
        self.update_good_url = '/good/update_good/'
        self.down_good_url = '/good/down_good/'
        self.get_good_code_list_url = '/good/get_good_code_list/'

        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_good_detail_api(self):
        request = self.request.get(self.get_good_detail_url, {'good_id': 1
                                                              })
        request.user = self.user
        response = GoodViewSet().get_good_detail(request)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_good_list_api(self):
        request = self.request.get(self.get_good_list_url, {'good_name': 1
                                                            })
        request.user = self.user
        response = GoodViewSet().get_good_list(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_add_good_api(self):
        request = self.request.post(self.add_good_url, data={
            "good_code": "ASD-111",
            "good_name": "电脑",
            "good_type_id": 1,
            "price": 3.6,
            "pics": "https://gitee.com/mypassion/fileimage/blob/master/images/2.png",
            "introduce": "123",
            "remark": "123",
            "specifications": "456"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GoodViewSet().add_good(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_update_good_api(self):
        request = self.request.post(self.update_good_url, data={
            "id": 1,
            "good_code": "ASD-111",
            "good_name": "电脑",
            "good_type_id": 1,
            "price": 6.3,
            "pics": "https://gitee.com/mypassion/fileimage/blob/master/images/2.png",
            "introduce": "123",
            "remark": "123",
            "specifications": "456"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        print(request.data)
        response = GoodViewSet().update_good(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_down_good_api(self):
        request = self.request.post(self.down_good_url, data={
            "id": 1,
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GoodViewSet().down_good(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_good_code_list_api(self):
        request = self.request.post(self.down_good_url, data={})
        request.user = self.user
        response = GoodViewSet().get_good_code_list(request)
        self.assertEqual(response.status_code, 200)


class CartModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.goodtype_obj = GoodType.objects.create(type_name="办公用品")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = Good.objects.create(good_code="ASN-123", good_name="桌子", good_type_id=1,
                                            price=3.6,
                                            pics="https://gitee.com/mypassion/fileimage/raw/master/images/1.png",
                                            introduce="test", remark="test2", specifications="test3")
        self.cart_obj = Cart.objects.create(id=1, username="3190911048X", good_id=1, num=3)

        self.add_cart_goods_url = '/cart/add_cart_goods/'
        self.update_cart_goods_url = '/cart/update_cart_goods/'
        self.delete_cart_goods_url = '/cart/delete_cart_goods/'
        self.get_shopping_cart_url = '/cart/get_shopping_cart/'
        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_add_cart_goods_api(self):
        request = self.request.post(self.add_cart_goods_url, data={
            "goodInfo": {
                "num": 1,
                "id": 1
            }
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = CartViewSet().add_cart_goods(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_update_cart_goods_api(self):
        request = self.request.post(self.update_cart_goods_url, data={
            "goodsList": [
                {
                    "num": 6,
                    "id": 1
                }
            ]
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = CartViewSet().update_cart_goods(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_delete_cart_goods_api(self):
        request = self.request.post(self.delete_cart_goods_url, data={
            "cartIdList": [1]
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)

        response = CartViewSet().delete_cart_goods(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_shopping_cart_api(self):
        request = self.request.post(self.get_shopping_cart_url, {'username': "3190911048X"
                                                                 })
        request.user = self.user
        response = CartViewSet().get_shopping_cart(request)
        self.assertEqual(response.status_code, 200)


class WithdrawModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.goodtype_obj = GoodType.objects.create(type_name="办公用品")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = Good.objects.create(good_code="ASN-123", good_name="桌子", good_type_id=1,
                                            price=3.6,
                                            pics="https://gitee.com/mypassion/fileimage/raw/master/images/1.png",
                                            introduce="test", remark="test2", specifications="test3")
        self.cart_obj = Cart.objects.create(id=1, username="3190911048X", good_id=1, num=3)
        self.apply_obj = Withdraw.objects.create(good_apply_id=1, username="3190911048", reason_id=1, position="西安",
                                                 remark="退货申请尽快办理", status=0)

        self.add_withdraw_apply_url = '/withdraw/add_withdraw_apply/'
        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_add_withdraw_apply_api(self):
        request = self.request.post(self.add_withdraw_apply_url, data={
            "good_ids": [1],
            "reason_id": 1,
            "position": "西安",
            "remark": "尽快办理"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = WithdrawViewSet().add_withdraw_apply(request)
        self.assertEqual(response.status_code, 200)


class WithdrawReasonModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.goodtype_obj = GoodType.objects.create(type_name="办公用品")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = Good.objects.create(good_code="ASN-123", good_name="桌子", good_type_id=1,
                                            price=3.6,
                                            pics="https://gitee.com/mypassion/fileimage/raw/master/images/1.png",
                                            introduce="test", remark="test2", specifications="test3")
        self.cart_obj = Cart.objects.create(id=1, username="3190911048X", good_id=1, num=3)
        self.apply_obj = Withdraw.objects.create(good_apply_id=1, username="3190911048", reason_id=1, position="西安",
                                                 remark="退货申请尽快办理", status=0)
        self.reason_obj = WithdrawReason.objects.create(reason_type="业务调整")
        self.list_url = '/withdraw_reason/'
        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_add_withdraw_apply_api(self):
        request = self.request.get(self.list_url, data={
        })
        request.user = self.user
        response = WithdrawReasonViewSet().list(request)
        self.assertEqual(response.status_code, 200)


class GroupApplyReasonModelTestCase(TestCase):
    def setUp(self):
        self.edit_obj = UserInfo.objects.create(username="3190911048X", phone="15029747733", position="西安")
        self.goodtype_obj = GoodType.objects.create(type_name="办公用品")
        self.user = User.objects.create_superuser(username="3190911048X", password="825278297xSw")
        self.good_obj = Good.objects.create(good_code="ASN-123", good_name="桌子", good_type_id=1,
                                            price=3.6,
                                            pics="https://gitee.com/mypassion/fileimage/raw/master/images/1.png",
                                            introduce="test", remark="test2", specifications="test3")
        self.cart_obj = Cart.objects.create(id=1, username="3190911048X", good_id=1, num=3)
        self.apply_obj = Withdraw.objects.create(good_apply_id=1, username="3190911048", reason_id=1, position="西安",
                                                 remark="退货申请尽快办理", status=0)
        self.reason_obj = WithdrawReason.objects.create(reason_type="业务调整")
        self.groupapply_obj = GroupApply.objects.create(good_code="ASN-124", num=2, username="3190911048X",
                                                        position="深圳"
                                                        , phone="15029747733", status=4)
        self.groupapply_obj = GroupApply.objects.create(good_code="ASN-123", num=1, username="3190911048X",
                                                        position="深圳"
                                                        , phone="15029747733", status=5)
        self.get_group_apply_url = '/group_apply/get_group_apply/'
        self.delete_group_apply_url = '/group_apply/delete_group_apply/'
        self.update_group_apply_url = '/group_apply/update_group_apply/'
        self.get_personal_goods_url = '/group_apply/get_personal_goods/'
        self.get_personal_goods_url = '/group_apply/get_personal_goods/'
        self.get_good_status_list_url = '/group_apply/get_good_status_list/'

        self.request = RequestFactory()

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_group_apply_api(self):
        request = self.request.get(self.get_group_apply_url, data={
        })
        request.user = self.user
        response = WithdrawReasonViewSet().list(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_delete_group_apply_api(self):
        request = self.request.post(self.delete_group_apply_url, data={
            "applyId": 1
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GroupApplyViewSet().delete_group_apply(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_update_group_apply_api(self):
        request = self.request.post(self.update_group_apply_url, data={
            "applyList": [
                {
                    "num": 2,
                    "id": 1
                }
            ],
            "updateType": "num"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GroupApplyViewSet().update_group_apply(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_personal_goods_api(self):
        request = self.request.post(self.get_personal_goods_url, data={
            "form": {
                "name": "桌子",
                "code": "ASN-123",
                "location": "西安",
                "status": 4,
                "type": "生活用品"
            },
            "page": 1,
            "pageLimit": 10,
            "idList": "[1]"
        }, content_type="application/json")
        request.user = self.user
        request.data = json.loads(request.body)
        response = GroupApplyViewSet().get_personal_goods(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_good_status_list_api(self):
        request = self.request.get(self.get_good_status_list_url, data={
        })
        request.user = self.user
        response = GroupApplyViewSet().get_good_status_list(request)
        self.assertEqual(response.status_code, 200)

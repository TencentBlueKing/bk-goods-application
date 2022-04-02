import json

from apps.good_apply.models import Apply, Position, Review, Secretary
from apps.good_apply.views import ApplyViewSet
from blueapps.account.models import User
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

TEST_MIDDLEWARE = (
    "blueapps.utils.request_provider.RequestProvider",
)


class SecretaryModelTestCase(TestCase):
    """
    秘书表的测试类
    """

    def setUp(self):
        """创建不同类型的model对象"""
        self.obj = Secretary.objects.create(username='admin')


class PositionModelTestCase(TestCase):
    def setUp(self):
        """创建不同类型的model对象"""
        self.p_obj = Position.objects.create(position_code='xxx1', name='省级地区', parent_code=None)
        self.c_obj = Position.objects.create(position_code='xxx2', name='市级地区', parent_code='xxx1')

        self.get_root_position_list_url = '/position/get_root_position_list/'
        self.get_sub_position_list_url = '/position/get_sub_position_list/'

    # model测试

    def test_find_parent_from_child(self):
        """测试根据母地区代码获取地区"""
        parent = Position.objects.filter(position_code=self.c_obj.parent_code).first()
        self.assertEqual(self.p_obj.name, parent.name)

    def test_to_json(self):
        """测试序列化数据是否标准"""
        expect_result = {
            "id": self.c_obj.id,
            "code": self.c_obj.position_code,
            "name": self.c_obj.name
        }
        self.assertEqual(Position.to_json(self.c_obj), expect_result)

    # 接口测试

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_root_position_list_api(self):
        """测试获取根地址接口"""
        response = self.client.get(self.get_root_position_list_url)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def get_sub_position_list_api(self):
        """测试获取子地区接口"""
        objs = Position.objects.filter(parent_code='xxx1')
        expect_data = list()
        for item in objs:
            expect_data.append(
                {
                    'id': item.id,
                    'code': item.position_code,
                    'name': item.name
                }
            )
        expect_result = {
            "code": "200",
            "result": True,
            "message": "success",
            "data": expect_data
        }
        response = self.client.get(self.get_sub_position_list_url, {'parent_code': 'xxx1'})
        self.assertEqual(response.json(), expect_result)


class ApplyModelTestCase(TestCase):
    """
    申请表测试类
    """

    def setUp(self):
        """创建不同类型的model对象"""
        self.stop_obj = Apply.objects.create(good_code='TEST1', good_name="测试物品1", num=5, require_date='2021-3-14',
                                             reason='测试用例', position='广东，广州', status=0, apply_user='admin')
        self.secretary_examining_obj = Apply.objects.create(good_code='TEST3', good_name="测试物品3", num=5,
                                                            require_date='2021-3-14', reason='测试用例',
                                                            position='广东，广州', status=1, apply_user='admin')
        self.done_obj = Apply.objects.create(good_code='TEST4', good_name="测试物品4", num=5, require_date='2021-3-14',
                                             reason='测试用例', position='广东，广州', status=2, apply_user='admin')

        self.request = RequestFactory()
        self.user = User.objects.create_superuser(username='admin', password='123456')

        self.submit_apply_list_url = '/apply/submit_apply_list/'
        self.get_apply_url = '/apply/'
        self.update_good_apply_url = '/apply/update_good_apply/'
        self.stop_good_apply_url = '/apply/stop_good_apply/'
        self.delete_good_apply_url = '/apply/{id}/delete_good_apply/'.format(id=self.stop_obj.id)
        self.get_apply_status_url = '/apply/get_apply_status/'
        self.get_self_good_apply_list_url = '/apply/get_self_good_apply_list/'
        self.examine_apply_url = '/apply/examine_apply/'

    # model测试

    def test_get_status_display(self):
        """测试枚举类型文字是否符合"""
        self.assertEqual(self.stop_obj.get_status_display(), '申请终止')
        self.assertEqual(self.secretary_examining_obj.get_status_display(), '管理员审核中')
        self.assertEqual(self.done_obj.get_status_display(), '审核完成')

    def test_to_json(self):
        """测试序列化数据是否标准"""
        expect_result = {
            "id": self.done_obj.id,
            "good_code": self.done_obj.good_code,
            "good_name": self.done_obj.good_name,
            "num": self.done_obj.num,
            "require_date": self.done_obj.require_date,
            "reason": self.done_obj.reason,
            "position": self.done_obj.position,
            "status": self.done_obj.get_status_display(),
            "apply_user": self.done_obj.apply_user,
            "apply_time": self.done_obj.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.assertEqual(Apply.to_json(self.done_obj), expect_result)

    # 接口测试

    # TODO:蓝鲸官方接口权限校验
    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    # def test_submit_apply_list_api(self):
    #     request = self.request.post(path=self.submit_apply_list_url, data={
    #         "apply_list": [
    #                 {
    #                     "id": 1,
    #                     "num": 3,
    #                     "good_code": "unit test",
    #                     "good_name": "单元测试",
    #                     "require_date": "2023-03-31",
    #                     "apply_user": "admin",
    #                     "leaders": "无",
    #                     "school": "广东",
    #                     "academy": "广州",
    #                     "detail_position": "guangzhou",
    #                     "reason": "unit test"
    #                 }
    #         ]
    #     }, content_type="application/json")
    #     request.user = self.user
    #     request.data = json.loads(request.body)
    #     response = ApplyViewSet().submit_apply_list(request)
    #     self.assertEqual(response.status_code, 200)

    # TODO:蓝鲸官方接口权限校验
    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    # def test_apply_api(self):
    #     query = Q(status=2)
    #     applys = Apply.objects.filter(query).order_by("-update_time")
    #     paginator = Paginator(applys, 10)
    #     cur_applys = paginator.get_page(1)
    #
    #     expect_data = {"total_num": applys.count(),
    #             "apply_list": [apply.to_json() for apply in cur_applys]}
    #
    #     for item in expect_data['apply_list']:
    #         item['require_date'] = datetime.datetime.strftime(item['require_date'], "%Y-%m-%d")
    #
    #     expect_result = {
    #                         "code": "200",
    #                         "result": True,
    #                         "message": "success",
    #                         "data": expect_data,
    #                     }
    #     response = self.client.get(self.get_apply_url)
    #     self.assertEqual(response.json(), expect_result)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_self_good_apply_list_api(self):
        """测试获取自身申请记录接口"""
        request = self.request.get(self.get_self_good_apply_list_url, data={})
        request.user = self.user
        response = ApplyViewSet().get_self_good_apply_list(request)
        self.assertEqual(response.status_code, 200)

    # TODO:蓝鲸官方接口权限校验
    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    # def test_examine_apply_api(self):
    #     request = self.request.post(path=self.examine_apply_url, data={
    #         "apply_id_list": [
    #             self.secretary_examining_obj.id
    #         ],
    #         "model": "agree",
    #         "remark": "无"
    #     }, content_type="application/json")
    #     request.user = self.user
    #     request.data = json.loads(request.body)
    #     response = ApplyViewSet().examine_apply(request)
    #     self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_update_good_apply_api(self):
        """测试更新申请信息接口"""
        request = self.request.patch(path=self.update_good_apply_url, data={
            'id': self.secretary_examining_obj.id,
            'good_code': self.secretary_examining_obj.good_code,
            'good_name': self.secretary_examining_obj.good_name,
            'reason': 'unit test',
            'num': 99
        }, content_type="application/json")
        request.data = json.loads(request.body)
        response = ApplyViewSet().update_good_apply(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_stop_good_apply_api(self):
        """测试终结申请接口"""
        request = self.request.patch(path=self.stop_good_apply_url, data={'id': self.secretary_examining_obj.id},
                                     content_type="application/json")
        request.data = json.loads(request.body)
        response = ApplyViewSet().stop_good_apply(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_delete_good_apply_api(self):
        """测试删除申请接口"""
        response = self.client.delete(self.delete_good_apply_url)
        self.assertEqual(response.json()['code'], 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_apply_status_api(self):
        """测试获取所有申请状态接口"""
        response = self.client.get(self.get_apply_status_url)
        self.assertEqual(response.json()['code'], 200)


class ReviewModelTestCase(TestCase):
    """
    审核表测试类
    """

    def setUp(self):
        """创建不同类型的model实例"""
        self.secretary_success_obj = Review.objects.create(apply_id=1, reviewer='admin',
                                                           reviewer_identity=2, result=1, reason='单元测试')
        self.secretary_fail_obj = Review.objects.create(apply_id=1, reviewer='admin',
                                                        reviewer_identity=2, result=2, reason='单元测试')

    # model测试

    def test_get_reviewer_identity_display(self):
        """创建不同类型的model实例"""
        self.assertEqual(self.secretary_success_obj.get_reviewer_identity_display(), '管理员')

    def test_get_result_display(self):
        """测试枚举类型文字是否符合"""
        self.assertEqual(self.secretary_success_obj.get_result_display(), '通过')
        self.assertEqual(self.secretary_fail_obj.get_result_display(), '未通过')

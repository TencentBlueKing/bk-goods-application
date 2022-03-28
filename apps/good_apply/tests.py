import requests
from apps.good_apply.models import Apply, Position, Review, Secretary
from django.test import TestCase
from django.test.utils import override_settings

TEST_MIDDLEWARE = (
    "blueapps.utils.request_provider.RequestProvider",
)


class SecretaryModelTestCase(TestCase):
    def setUp(self):
        self.obj = Secretary.objects.create(username='790795324Q')


class PositionModelTestCase(TestCase):
    def setUp(self):
        self.p_obj = Position.objects.create(position_code='xxx1', name='省级地区', parent_code=None)
        self.c_obj = Position.objects.create(position_code='xxx2', name='市级地区', parent_code='xxx1')

        self.get_root_position_list_url = '/position/get_root_position_list/'
        self.get_sub_position_list_url = '/position/get_sub_position_list/'

    # model测试

    def test_find_parent_from_child(self):
        parent = Position.objects.filter(position_code=self.c_obj.parent_code).first()
        self.assertEqual(self.p_obj.name, parent.name)

    def test_to_json(self):
        expect_result = {
            "id": self.c_obj.id,
            "code": self.c_obj.position_code,
            "name": self.c_obj.name
        }
        self.assertEqual(Position.to_json(self.c_obj), expect_result)

    # 接口测试

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_root_position_list_api(self):
        objs = Position.objects.filter(parent_code=None)
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
            "code": 200,
            "result": True,
            "message": "success",
            "data": expect_data
        }
        response = self.client.get(self.get_root_position_list_url)
        self.assertEqual(response.json(), expect_result)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def get_sub_position_list_api(self):
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
    def setUp(self):
        self.stop_obj = Apply.objects.create(good_code='TEST1', good_name="测试物品1", num=5, require_date='2021-3-14',
                                             reason='测试用例', position='广东，广州', status=0, apply_user='790795324Q')
        self.leader_examining_obj = Apply.objects.create(good_code='TEST2', good_name="测试物品2", num=5,
                                                         require_date='2021-3-14', reason='测试用例',
                                                         position='广东，广州', status=1, apply_user='790795324Q')
        self.secretary_examining_obj = Apply.objects.create(good_code='TEST3', good_name="测试物品3", num=5,
                                                            require_date='2021-3-14', reason='测试用例',
                                                            position='广东，广州', status=2, apply_user='790795324Q')
        self.done_obj = Apply.objects.create(good_code='TEST4', good_name="测试物品4", num=5, require_date='2021-3-14',
                                             reason='测试用例', position='广东，广州', status=3, apply_user='790795324Q')

        self.session = requests.Session()
        # self.client = APIClient()
        # self.user = User.objects.create_superuser(username='790795324Q', password='123456')
        # self.client.force_login(self.user)
        self.submit_apply_list_url = 'http://dev.paas-edu.bktencent.com:8000/apply/submit_apply_list/'
        self.get_apply_url = '/apply/'
        self.stop_good_apply_url = '/apply/stop_good_apply/'
        self.delete_good_apply_url = '/apply/2/delete_good_apply/'
        self.get_apply_status_url = '/apply/get_apply_status/'

    # model测试

    def test_get_status_display(self):
        self.assertEqual(self.stop_obj.get_status_display(), '申请终止')
        self.assertEqual(self.leader_examining_obj.get_status_display(), '导员审核中')
        self.assertEqual(self.secretary_examining_obj.get_status_display(), '管理员审核中')
        self.assertEqual(self.done_obj.get_status_display(), '审核完成')

    def test_to_json(self):
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

    # TODO:有问题
    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    # def test_submit_apply_list_api(self):
    #     response = self.client.post(self.submit_apply_list_url, {
    #         "apply_list": [
    #                 {
    #                     "id": 1,
    #                     "num": 3,
    #                     "good_code": "unit test",
    #                     "good_name": "单元测试",
    #                     "require_date": "2023-03-31",
    #                     "apply_user": "790795324Q",
    #                     "leaders": "无",
    #                     "school": "广东",
    #                     "academy": "广州",
    #                     "detail_position": "guangzhou",
    #                     "reason": "unit test"
    #                 }
    #         ]
    #     })
    #     print('response', response.json())
    #     self.assertEqual(response.status_code, 200)

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

    # TODO:有问题
    # @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    # def test_stop_good_apply_api(self):
    #     response = self.client.patch(self.stop_good_apply_url, {id: 3})
    #     print('response', response)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_delete_good_apply_api(self):
        response = self.client.delete(self.delete_good_apply_url)
        self.assertEqual(response.json()['code'], 200)

    @override_settings(MIDDLEWARE=TEST_MIDDLEWARE)
    def test_get_apply_status_api(self):
        response = self.client.get(self.get_apply_status_url)
        self.assertEqual(response.json()['code'], 200)


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.leader_success_obj = Review.objects.create(apply_id=1, reviewer='790795324Q',
                                                        reviewer_identity=1, result=1, reason='单元测试')
        self.leader_fail_obj = Review.objects.create(apply_id=1, reviewer='790795324Q',
                                                     reviewer_identity=1, result=2, reason='单元测试')
        self.secretary_success_obj = Review.objects.create(apply_id=1, reviewer='790795324Q',
                                                           reviewer_identity=2, result=1, reason='单元测试')
        self.secretary_fail_obj = Review.objects.create(apply_id=1, reviewer='790795324Q',
                                                        reviewer_identity=2, result=2, reason='单元测试')

    # model测试

    def test_get_reviewer_identity_display(self):
        self.assertEqual(self.leader_success_obj.get_reviewer_identity_display(), '导员')
        self.assertEqual(self.secretary_success_obj.get_reviewer_identity_display(), '管理员')

    def test_get_result_display(self):
        self.assertEqual(self.leader_success_obj.get_result_display(), '通过')
        self.assertEqual(self.leader_fail_obj.get_result_display(), '未通过')

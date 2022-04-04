from celery.schedules import crontab
from celery.task import periodic_task, task
from django.conf import settings


@periodic_task(run_every=crontab(minute="*/15", hour="20"))
def add_member_from_bk_usermanagement(inner_list=settings.INNER_LIST):
    """
    从蓝鲸用户管理系统拉人
    inner_list: 内部组表
    """
    print("SUCCESS:", inner_list)


@task()
def send_email(client, receiver_list, title, content):
    """
    发送邮件
    request：网络请求
    receiver_list：接收者邮箱列表
    title：邮件主题
    content：邮件内容
    """
    receiver_str = ','.join(receiver_list)
    client.cmsi.send_mail(title=title, content=content, receiver=receiver_str)

    # receiver_str = ','.join(['790795324@qq.com'])
    # client = get_client_by_request(request=self.request)
    # client.cmsi.send_mail(title='testdelay', content='testdelay', receiver=receiver_str)

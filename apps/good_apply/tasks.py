from blueapps.core.celery.celery import app
from blueapps.utils import get_client_by_request


@app.task(bind=True)
def add_member_from_bk_usermanagement(self, inner_list):
    """
    从蓝鲸用户管理系统拉人
    inner_list: 内部组表
    """
    pass


@app.task(bind=True)
def send_email(self, request, receiver_list, title, content):
    """
    发送邮件
    request：网络请求
    receiver_list：接收者邮箱列表
    title：邮件主题
    content：邮件内容
    """
    receiver_str = ','.join(receiver_list)
    client = get_client_by_request(request=request)
    client.cmsi.send_mail(title=title, content=content, receiver=receiver_str)

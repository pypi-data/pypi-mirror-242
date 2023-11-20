from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime

from ats_case.case.atm import extract_letters
from ats_base.service import db

TXT = '### **自动化测试报告**\n\n---\n\n>**测试序号:**  {}\n\n>**测试结果:**  {}\n\n>**发送时间:**  {}\n\n'


def send(test_sn: str, payload: str):
    url, secret, sign = _link(test_sn)
    dc = DingtalkChatbot(url, secret)
    result = dc.send_markdown(title=f'{sign}', text=_data(payload, test_sn), is_at_all=True)
    print(result)


def _link(test_sn):
    username = extract_letters(test_sn)

    user = db.query('sys:user', name=username)
    gid = user.get('msg_group_id')
    group = db.query('sys:msg:group', id=gid)

    url = group.get('url')
    secret = group.get('secret')
    sign = group.get('sign')

    return url, secret, sign


def _data(payload, test_sn):
    sn = test_sn.split(':')[0]
    if payload == 'normal':
        return _normal(sn)
    if payload == 'warn':
        return _warn(sn)
    if payload == 'error':
        return _error(sn)


def _normal(sn):
    completed_msg = '<font color="#00EE00">[完成]</font>'
    now_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    return TXT.format(sn, completed_msg, now_time)


def _warn(sn):
    completed_msg = '<font color="#00EE00">[警告]</font>'
    now_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    return TXT.format(sn, completed_msg, now_time)


def _error(sn):
    completed_msg = '<font color="#00EE00">[出错]</font>'
    now_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    return TXT.format(sn, completed_msg, now_time)

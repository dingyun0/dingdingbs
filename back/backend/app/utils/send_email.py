#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from backend.app.common.log import log
from backend.app.core.conf import Settings
from backend.app.utils.generate_string import get_uuid4_str

__only_code = get_uuid4_str()

SEND_RESET_PASSWORD_TEXT = f'您的重置密码验证码为：{__only_code}\n为了不影响您正常使用，请在{int(Settings.COOKIES_MAX_AGE / 60)}分钟内完成密码重置'  # noqa: E501


async def send_verification_code_email(to: str, code: str, text: str = SEND_RESET_PASSWORD_TEXT):
    """
    发送验证码电子邮件

    :param to:
    :param code:
    :param text:
    :return:
    """
    text = text.replace(__only_code, code)
    msg = MIMEMultipart()
    msg['Subject'] = Settings.EMAIL_DESCRIPTION
    msg['From'] = Settings.EMAIL_USER
    msg.attach(MIMEText(text, _charset='utf-8'))

    # 登录smtp服务器并发送邮件
    try:
        smtp = aiosmtplib.SMTP(hostname=Settings.EMAIL_SERVER,
                               port=Settings.EMAIL_PORT, use_tls=Settings.EMAIL_SSL)
        async with smtp:
            await smtp.login(Settings.EMAIL_USER, Settings.EMAIL_PASSWORD)
            await smtp.sendmail(msg['From'], to, msg.as_string())
            await smtp.quit()
    except Exception as e:
        log.error('邮件发送失败 {}', e)
        raise Exception('邮件发送失败 {}'.format(e))

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText

_sender = 'peiyuc@sina.com'
_subject = '余票不足'
_smtpserver = 'smtp.sina.com'
_username = 'peiyuc@sina.com'
_password = 'cpy3869552'


def sendMail(subject, receiver,  content):
    msg = MIMEText(content)
    msg['Subject'] = subject + _subject
    smtp = smtplib.SMTP()
    smtp.connect(_smtpserver)
    smtp.login(_username, _password)
    smtp.sendmail(_sender, receiver, msg.as_string())
    smtp.quit()
    print 'send success'

#sendMail('hi')

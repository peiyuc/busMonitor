#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText

_sender = '***'
_subject = '余票不足'
_smtpserver = 'smtp.sina.com'
_username = '***'
_password = '***'


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

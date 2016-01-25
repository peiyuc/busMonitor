#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import urllib2
from sgmllib import SGMLParser
import MailSender


class BusHtmlParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.isTime = False
        self.isPrice = False
        self.isRemindTicket = False
        self.isFrom = False
        self.isTo = False
        self.bus = []

    def start_span(self, attrs):
        if len(attrs) == 0:
            pass
        else:
            for (valText, val) in attrs:
                if valText == 'class' and val == 'lv_time':
                    self.isTime = True
                elif valText == 'class' and val == 'tk_price':
                    self.isPrice = True
                elif valText == 'class' and (val == 'tk_remain' or val == 'tk_remain1'):
                    self.isRemindTicket = True
                elif valText == 'class' and val == 'st_from':
                    self.isFrom = True
                elif valText == 'class' and val == 'st_to':
                    self.isTo = True

    def end_span(self):
        self.isTime = False
        self.isPrice = False
        self.isRemindTicket = False
        self.isFrom = False
        self.isTo = False

    def handle_data(self, data):
        if self.isTime or self.isPrice or self.isFrom or self.isTo:
            self.bus.append(data.strip())
        elif self.isRemindTicket and len(data.strip()) <=2:
            self.bus.append(data.strip())


startStation = ['320500003', '320500004']
dates = ['2016-02-02', '2016-02-03', '2016-02-04', '2016-02-05', '2016-02-06']
params = {'bigCategory': '3205000', 'smallCategory': '320500003', 'dst_name': '淮安', 'drive_date': '2016-01-26',
          'x': '51', 'y': '13', 'from': '苏州'}


def getUrlContent(params):
    url = 'http://www.szqcz.com/busSearch.do'
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)
    parser = BusHtmlParser()
    parser.feed(resp.read())
    return parser


def parseStation(dates, startStation, params):
    desc = ''
    for station in startStation:
        for date in dates:
            print date, station
            params['smallCategory'] = station
            params['drive_date'] = date
            desc = desc + '\n' + parse(params)
    return desc


def parse(params):
    parser = getUrlContent(params)
    ticket = parser.bus
    ticketDesc = ''
    isFirstItem = True
    for i in range(len(ticket) / 5):
        if int(ticket[5 * i + 4]) < 20:
            desc = '{0} {1} 从 {2} 到 {3} 票价 {4} 只剩 {5}'.format(params['drive_date'], ticket[5 * i + 2], ticket[5 * i], ticket[5 * i + 1], ticket[5 * i + 3], ticket[5 * i + 4])
            if isFirstItem:
                ticketDesc = desc
            else:
                ticketDesc = ticketDesc + "\n" + desc
            isFirstItem = False
    return ticketDesc

desc = parseStation(dates, startStation, params)

_receiver = ['812653775@qq.com', '530795037@qq.com']

if len(desc) < 10:
    print '客票数量正常,无需提醒'
else:
    MailSender.sendMail(params['from'] + "到" + params['dst_name'], _receiver, desc)

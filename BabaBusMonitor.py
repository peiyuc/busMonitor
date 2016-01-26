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
        self.isPagerNum = False
        self.bus = []
        self.pageNum = -1

    def start_p(self, attrs):
        if len(attrs) == 0:
            pass
        else:
            for (valText, val) in attrs:
                if valText == 'class' and val == 'stime':
                    self.isTime = True

    def end_p(self):
        self.isTime = False

    def start_li(self, attrs):
        if len(attrs) == 0:
            pass
        else:
            for (valText, val) in attrs:
                if valText == 'class' and val == 'serlist_bd_tprice':
                    self.isPrice = True
                elif valText == 'class' and val == 'serlist_bd_tyupiao':
                    self.isRemindTicket = True

    def end_li(self):
        self.isPrice = False
        self.isRemindTicket = False

    def start_span(self, attrs):
        if len(attrs) == 0:
            pass
        else:
            for (valText, val) in attrs:
                if valText == 'class' and val == 'pager_jump_text':
                    self.isPagerNum = True

    def end_span(self):
        self.isPagerNum = False

    def handle_data(self, data):
        if self.isTime or self.isPrice or self.isRemindTicket:
            self.bus.append(data.strip())
        elif self.isPagerNum and self.pageNum == -1:
            self.pageNum = data[4]


dates = ['2016-02-02', '2016-02-03', '2016-02-04', '2016-02-05', '2016-02-06']
params = {'from': '杭州', 'to': '兴化', 'date': '2016-01-25', 'page': '1'}


def getUrlContent(params):
    url = 'http://www.bababus.com/baba/ticket/ticketList.htm'
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    resp = urllib2.urlopen(req)
    parser = BusHtmlParser()
    parser.feed(resp.read())
    return parser

def parse(dates, params):
    desc = ''
    for date in dates:
        print date
        params['date'] = date
        singleDesc = parseSingle(params)
        desc = desc + '\n' + singleDesc
    return desc

def parseSingle(params):
    parser = getUrlContent(params)
    pageSize = int(parser.pageNum)
    ticket = parser.bus
    for i in range(pageSize):
        if i > 0:
            params['page'] = i + 1
            parserTemp = getUrlContent(params)
            for val in parserTemp.bus:
                ticket.append(val)

    ft = []
    for val in ticket:
        if len(val) > 0 and val != '\xef\xbf\xa5':
            ft.append(val)

    ticketDesc = ''
    isFirstItem = True
    for i in range(len(ft) / 3):
        if int(ft[3*i+2]) < 20:
            desc = '{0} {1} 票价 {2} 只剩 {3}'.format(params['date'], ft[3*i], ft[3*i+1], ft[3*i+2])
            if isFirstItem:
                ticketDesc = desc
            else:
                ticketDesc = ticketDesc + "\n" + desc
            isFirstItem = False
    return ticketDesc

desc = parse(dates, params)

_receiver = ['***']

if len(desc) < 10:
    print '客票数量正常,无需提醒'
else:
    MailSender.sendMail(params['from'] + "到" + params['to'], _receiver, desc)

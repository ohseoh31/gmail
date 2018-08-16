import smtplib
import time
import imaplib
import email
import re
import os
import urllib3
import urllib.request
import requests
from datetime import datetime
import datetime
from openpyxl import Workbook
import hashlib

import gpsParser

#dic
short_url_list = {
    "https://hoy.kr/" : 4,
    "http://hoy.kr/" : 4,
    "https://bit.ly/" : 7,
    "http://bit.ly/" : 7,
    "https://bitly.kr/" : 4,
    "http://bitly.kr/" : 4,
    "https://goo.gl/" : 6,
    "http://goo.gl/" : 6
}

login_info= {
    'ORG_EMAIL' : '@gmail.com',
    'FROM_EMAIL' : '[YOUR_EMAIL_ID]@gmail.com',
    'FROM_PWD' : '[YOUR_PASSWRD]',
    'SMTP_SERVER' : "imap.gmail.com",
    'SMTP_PORT' : 993
}

class Gmail :
    def __init__(self,login_info):
        self.loginInfo = login_info
        self.file_nameList = []
        self.date_time =''
        self.short_urlList = []
        self.full_urlList = []

        self.email_date = ''
        self.email_dateList =[]
    
    #gmail 계정 로그인
    def connect_gmail(self, mail):
        mail = imaplib.IMAP4_SSL(self.loginInfo['SMTP_SERVER'])
        mail.login(self.loginInfo['FROM_EMAIL'], self.loginInfo['FROM_PWD'])
        mail.select('inbox')
        return mail.search(None, 'ALL')

    # 이메일 하나의 정보 읽어오기
    def read_email_from_gmail(self):
        mail = imaplib.IMAP4_SSL(self.loginInfo['SMTP_SERVER'])
        mail.login(self.loginInfo['FROM_EMAIL'], self.loginInfo['FROM_PWD'])
        mail.select('inbox')
        type, data = self.connect_gmail(mail)
        mail_ids = data[0]
        id_list = mail_ids.split()
        for i in reversed(id_list):
            type, data = mail.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    # TODO byte UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbc
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_from = msg['from']

                    self.email_date = msg['date']
                    self.email_date = email.utils.parsedate(self.email_date)
                    self.email_date = time.mktime(self.email_date)
                    self.email_date = datetime.datetime.fromtimestamp(self.email_date) + datetime.timedelta(hours=9)

                    email_now=self.email_date.strftime('%Y-%m-%d')
                    check_time = datetime.datetime.now().strftime("%Y-%m-%d")

                    print (email_now)

                    #if email_from == 'Kyle Choi <fl0ckfl0ck@hotmail.com>' and '2018-08-11' == email_now:
                    if email_from == 'Kyle Choi <fl0ckfl0ck@hotmail.com>' and check_time == email_now:
                        print('From : ' + email_from + '\n')
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                self.find_shorUrl(part)

    # 단축 URL 가져오기
    def find_shorUrl(self,part):
        try :
            text = ''
            #body = part.get_payload()
            #text += body
            text += part.get_payload()
            re_x = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}?'
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}', text)
            for url in urls:
                for short_url in short_url_list:
                    if short_url in url:

                        in_url = short_url + url[len(short_url):len(short_url) + short_url_list[short_url]]
                        print("connect url info : ", in_url)
                        # 이미지 다운로드
                        self.checkUrl(in_url)
        except UnicodeDecodeError :
            print ("From : UnicodeDecodeError Next\n")

    #URL 접속 확인 및 접속 URL이 fl0ckfl0ck.info인지 확인
    def checkUrl(self,url):
        req = requests.get(url)

        print ("접속 url : ",  req.url)
        if req.status_code == 200 and req.url.split('/')[2] =='fl0ckfl0ck.info':
            for short in self.short_urlList:
                if short == url :
                    return 0
            self.short_urlList.append(url)
            self.email_dateList.append(self.email_date)
            self.downloadImage(req, url)

    # 이미지 다운로드
    def downloadImage(self, req, url):
        now = datetime.datetime.now()
        path = str(now.year) + "_" + str(now.month) + "_" + str(now.day)

        outfile = self.url_decode(req)  # 파일명
        outpath = ".\\" + path + "\\"  # 저장 경로
        imagepath = ".\\image\\"
        #outpath = ".\\" + '2018_8_11' + "\\"  # 저장 경로
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        if not os.path.isdir(imagepath):
            os.makedirs(imagepath)

        # print (outfile[:-4]
        if outfile[(len(outfile) - 3):] == 'jpg' or outfile[(len(outfile) - 3):] == 'png' \
                or outfile[(len(outfile) - 3):] == 'bmp':
            urllib.request.urlretrieve(url, outpath + outfile)
            urllib.request.urlretrieve(url, imagepath + outfile)
            self.file_nameList.append(outfile)

    def url_decode(self, r):
        file_name = r.url
        self.full_urlList.append(urllib.parse.unquote(file_name))
        file_name = urllib.parse.unquote(file_name.split('/')[3])
        return file_name





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

'''
할일
Q1) 메일 읽어들여서 해당날짜에 저장
Q2) py2exe를 이용하여 윈도우 실행파일로 만들 것(20점)
Q3) 윈도우 스케쥴러를 이용하여 매일 11:50, 23:50 실행파일이 동작하도록 만들 것(10점) 
Q4) 프로그램이 실행되면 “YYYY-MM-DD”의 형태로 디렉토리를 만들고 그날의 결과물을 모두 저장할 것(결과물 : 각 이미지파일, csv 파일, 20점) 

'''

#서비스 등록하기 2018.08.08
'''
Q5) 이미지파일의 EXIF 정보를 파싱하여 GPS 데이터를 추출한 뒤 구맵으로 표현할 것 (10점) 
http://qkqhxla1.tistory.com/497
'''

'''
남은 일들



Q6) 위 과제 모두 해결 후 selenium 라이브러리를 이용하여 위 과제를 해결 할 것(20점)
'''
#TODO 셀리늄 사용하기?
'''
구현완료
Q1) 프로그램은 한번 실행되면  “fl0ckfl0ck@hotmail.com"로부터 수신된 이메일의 본문에서 단축URL을 파싱하여 업로드된 이미지파일을 다운로드하는 기능을 구현할 것(20점) 

'''




# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
#https://codehandbook.org/how-to-read-email-from-gmail-using-python/
#

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

#TODO 다시 설정해야됨 안이쁨

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "ohseoh44" + ORG_EMAIL
FROM_PWD    = "soek1212!@"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

login_info= {
    ORG_EMAIL : '@gmail.com',
    FROM_EMAIL : 'ohseoh44' + ORG_EMAIL,
    FROM_PWD : 'soek1212!@',
    SMTP_SERVER : "imap.gmail.com",
    SMTP_PORT : 993
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

    def connect_gmail(self, mail):
        mail = imaplib.IMAP4_SSL(self.loginInfo[SMTP_SERVER])
        mail.login(self.loginInfo[FROM_EMAIL], self.loginInfo[FROM_PWD])
        mail.select('inbox')
        return mail.search(None, 'ALL')

    # 이메일 하나의 정보 읽어오기
    def read_email_from_gmail(self):
        mail = imaplib.IMAP4_SSL(self.loginInfo[SMTP_SERVER])
        mail.login(FROM_EMAIL, FROM_PWD)
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

                    #print (email_from)
                    #print (email_date)
                    print (email_now)
                    #print ()
                    #exit(1)

                    if email_from == 'Kyle Choi <fl0ckfl0ck@hotmail.com>' and check_time == email_now:
                        print('From : ' + email_from + '\n')
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                #print(part)
                                self.find_shorUrl(part)

    # 단축 URL 가져오기
    def find_shorUrl(self,part):
        try :
            text = ''
            body = part.get_payload(decode=True)
            text += body.decode('utf-8')
            re_x = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}?'
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}', text)
            for url in urls:
                for short_url in short_url_list:
                    if short_url in url:
                        in_url = short_url + url[len(short_url):len(short_url) + short_url_list[short_url]]
                        #print("connect url info : ", in_url)
                        # 이미지 다운로드
                        self.checkUrl(in_url)
        except UnicodeDecodeError :
            print ("From : UnicodeDecodeError Next\n")


    def checkUrl(self,url):
        req = requests.get(url)
        if req.status_code == 200:
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
        outpath = ".\\" + '2018_8_2' + "\\"  # 저장 경로
        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        # print (outfile[:-4]
        if outfile[(len(outfile) - 3):] == 'jpg':
            urllib.request.urlretrieve(url, outpath + outfile)
            self.file_nameList.append(outfile)


    def url_decode(self, r):
        file_name = r.url
        self.full_urlList.append(urllib.parse.unquote(file_name))
        file_name = urllib.parse.unquote(file_name.split('/')[3])
        return file_name





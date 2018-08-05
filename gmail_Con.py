import smtplib
import time
import imaplib
import email
import re
import os
import urllib3
import urllib.request
import json

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "ohseoh44" + ORG_EMAIL
FROM_PWD    = "soek1212!@"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
#https://codehandbook.org/how-to-read-email-from-gmail-using-python/
#

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

def connect_gmail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')
    return mail.search(None, 'ALL')
def read_email_from_gmail():
        count =0
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = connect_gmail()
        mail_ids = data[0]

        id_list = mail_ids.split()
        bodyList = []
        for i in reversed(id_list):
            type, data = mail.fetch(i, '(RFC822)' )
            for response_part in data:
                if isinstance(response_part, tuple):

                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_from = msg['from']
                    if email_from == 'Kyle Choi <fl0ckfl0ck@hotmail.com>' :
                        print('From : ' + email_from + '\n')
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                text = ''
                                body = part.get_payload(decode=True)
                                text +=body.decode('utf-8')
                                re_x =  'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}?'
                                urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/?.{4,7}' , text)
                                for url in urls :
                                    for short_url in short_url_list:
                                        if short_url in url:
                                            in_url = short_url + url[len(short_url):len(short_url) + short_url_list[short_url]]
                                            print (in_url)
                                            #TODO image Download
                                            count = count +1
                                            checkUrl(in_url, "https://naver.com",count)

def read_fileName() :
    print ("read")

def downloadImage(url,count):
    outpath = ".\\img" #경로
    outfile = "img_"+str(count) +".jpg" # 파일명
    if not os.path.isdir (outpath):
        os.makedirs(outpath)
    urllib.request.urlretrieve(url,outpath + outfile)
    print ("file : " +outfile +" is downloade")

def checkUrl (url, referer,count) :
    http = urllib3.PoolManager()
    req = http.request("GET",url)
    #print (req.encoding)
    #print (json.loads(req.data.decode('utf-8')))
    #print (req.data.decode('utf-8'))
    #print ("data : ",req.read())
    #if req.status == 200 :
    #    downloadImage(url, count)

        #req.add_header("Referer", referer)
        #response = urllib3.urlopen(req)
        #print(response)
    #http = urllib3.PoolManager()
    #req = http.request(url)
    #req.add_header("Referer", referer)
    #response = urllib3.urlopen(req)
    #print (response)
    #the_page = response.read()
    #except Exception:
    #    print ("Exception",Exception)


read_email_from_gmail()
import datetime
import os
import hashlib
from openpyxl import Workbook

import gpsParser
import gmail


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


#파일 경로 검색
def search(dirname):
    fileName_list = []
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.jpg' or ext == '.png' or ext == '.bmp':

                    fileName_list.append(full_filename)

        return fileName_list

    except PermissionError:
        print("permission Denided")
        pass

#CSV 엑셀파일 저장
def saveExcel(outpath,url,fileName):
    wb = Workbook()
    ws = wb.active
    ws.title = "download Img info"
    ws['A1'] = 'url 정보'
    ws['B1'] = '파일명'
    for i in range(0, len(url)):
        url_text = 'A' + str(i+2)
        ws[url_text] = url[i]

    for i in range(0, len(fileName)):
        fileName_text = 'B' + str(i+2)
        ws[fileName_text] = fileName[i]

    now = datetime.datetime.now()
    date = str(now.year) + "_" + str(now.month) + "_" + str(now.day)
    file = date + '.csv'
    wb.save(outpath+file)
    os.system("start %s" % (outpath+file))
    print ('excel_save')


#파일 MD5 해시값 얻기
def getHash_MD5(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

#파일 SHA1 해시값 얻기
def getHash_SHA1(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.sha1()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

if __name__ == "__main__":

    now = datetime.datetime.now()
    path = str(now.year) + "_" + str(now.month) + "_" + str(now.day)
    outpath = ".\\" + path + "\\"  # 저장 경로
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    '''
        다운로드 시간
        Short URL
        Full URL
        파일명
        파일 hash 값
    '''

    gmail = gmail.Gmail(login_info)
    gmail.read_email_from_gmail()

    print("email time : ", gmail.email_dateList)
    print ("file Name : ", gmail.file_nameList)
    print ("short url : ", gmail.short_urlList)
    print ("full url  : ", gmail.full_urlList)

    '''
        GPS정보 (lat , long)

    '''

    gpslist = []
    md5list = []
    sha1list= []
    gParser = gpsParser.GpsParser(gpslist)


    '''
        저장된 사진의 GPS 정보
        MD5 / SHA1 해시값
    '''

    fileName_list = search(outpath)
    for file in gmail.file_nameList:
        gps = gParser.getGPS(outpath +file)
        md5_hash = getHash_MD5(outpath +file)
        sha1_hash = getHash_SHA1(outpath +file)
        md5list.append(md5_hash)
        sha1list.append(sha1_hash)
        gpslist.append(gps)

    # 여부분을 엑셀로 저장한다?????

    print ('gpslist : ' ,gpslist)
    print('md5list : ', md5list)
    print('sha1list : ', sha1list)

    # TODO return value
    saveExcel(outpath, gmail.full_urlList, gmail.file_nameList)

    '''
        해당 날짜에서 받은 GPS 정보를 GPS 경로에 저장후 GPS 정보를 보여줌
    '''
    gParser.setGPSList(gpslist, gmail.file_nameList)
    gParser.setMap()
    gParser.getMap()

'''
'''
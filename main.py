import datetime
import os
import hashlib
from openpyxl import Workbook

import saveData
import gpsParser
import gmail

#TODO gmplot marker

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
    gmail = gmail.Gmail(gmail.login_info)
    gmail.read_email_from_gmail()


    '''
        저장된 사진의 GPS 정보
        MD5 / SHA1 해시값
    '''
    gpslist = []
    md5list = []
    sha1list= []
    gParser = gpsParser.GpsParser(gpslist)


    gmail.fileName_list = saveData.search(outpath)
    for file in gmail.file_nameList:
        gps = gParser.getGPS(outpath +file)
        md5_hash = saveData.getHash_MD5(outpath +file)
        sha1_hash = saveData.getHash_SHA1(outpath +file)
        md5list.append(md5_hash)
        sha1list.append(sha1_hash)
        gpslist.append(gps)

    # 여부분을 엑셀로 저장한다?????

    print ('gpslist : ' ,gpslist)
    print('md5list : ', md5list)
    print('sha1list : ', sha1list)
    excel_list = []

    excel_list.append(gmail.email_dateList)
    excel_list.append(gmail.file_nameList)
    excel_list.append(gmail.short_urlList)
    excel_list.append(gmail.full_urlList)
    excel_list.append(gpslist)
    excel_list.append(md5list)
    excel_list.append(sha1list)


    # 엑셀에 마지막 셀을 읽어들여 append
    saveData.saveExcel(outpath, excel_list)
    '''
        해당 날짜에서 받은 GPS 정보를 GPS 경로에 저장후 GPS 정보를 보여줌
    '''
    # https://console.cloud.google.com/google/maps-apis/api-list?project=my-speach-key&consoleReturnUrl=https:%2F%2Fcloud.google.com%2Fmaps-platform%2Fmaps%2F%3Fhl%3Dko&consoleUI=CLOUD&hl=ko&mods=metropolis_maps

    imageGPSList = []
    file_nameList = saveData.search('.\\image\\')
    for file in file_nameList:
        gps = gParser.getGPS(file)
        imageGPSList.append(gps)


    print ("file Name : ",file_nameList)

    gParser.setGPSList(imageGPSList, file_nameList)
    gParser.setMap()
    gParser.getMap()

'''
'''
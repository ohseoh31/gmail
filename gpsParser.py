#-*- coding: utf-8 -*-

import exifread
import folium
import os

'''
save gpsMap refer
http://qkqhxla1.tistory.com/497
https://python-visualization.github.io/folium/quickstart.html
'''
class GpsParser :
    def __init__(self, gpsList):
        self.gpsList = []
        self.fileNameList = []
        self.count =-1
    def setGPSList(self,gpsList,fileNameList):
        self.gpsList = gpsList
        self.fileNameList = fileNameList
    def setMap(self):
        #현재 우리나라 위치
        m = folium.Map(location=[37.49, 127.018],zoom_start=10)
        for file in self.fileNameList :
            print ('file :',file)
        for gps in self.gpsList:
            self.count = self.count +1
            if len(gps) !=0:
                folium.Marker(
                    location=gps,
                    popup= self.fileNameList[self.count],
                    icon=folium.Icon(icon='cloud')
                ).add_to(m)

        m.save('maps.html')

    def getMap(self):
        os.system('start maps.html')

    def _convert_to_degress(self, value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    def getGPS(self, filepath):
        '''
        returns gps data if present other wise returns empty dictionary
        '''
        with open(filepath, 'r') as f:
            tags = exifread.process_file(open(filepath, 'rb'))
            latitude = tags.get('GPS GPSLatitude')
            latitude_ref = tags.get('GPS GPSLatitudeRef')
            longitude = tags.get('GPS GPSLongitude')
            longitude_ref = tags.get('GPS GPSLongitudeRef')
            if latitude:
                lat_value = self._convert_to_degress(latitude)
                if latitude_ref.values != 'N':
                    lat_value = -lat_value
            else:
                return []
            if longitude:
                lon_value = self._convert_to_degress(longitude)
                if longitude_ref.values != 'E':
                    lon_value = -lon_value
            else:
                return []
            list = []
            list.append(lat_value)
            list.append(lon_value)
            return list
            #return [lat_value, lon_value]
        return []


#-*- coding: utf-8 -*-

import exifread
#import folium
import gmplot
import os

'''
save gpsMap refer
http://qkqhxla1.tistory.com/497
https://python-visualization.github.io/folium/quickstart.html
'''
class GpsParser:
    def __init__(self, gpsList):
        self.gpsList = []
        self.latitude_list = []
        self.longitude_list = []
        self.fileNameList = []
        self.count =-1
    def setGPSList(self,gpsList,fileNameList):
        self.gpsList = gpsList
        self.fileNameList = fileNameList

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

    def setMap(self):
        gmap3 = gmplot.GoogleMapPlotter(37.49,
                                        127.018, 13)
        count = -1
        for gps in self.gpsList:
            count = count + 1
            print (gps)
            if gps == []:
                continue
            else :
                fileName=str(self.fileNameList[count])
                gmap3.marker(gps[0], gps[1], 'red', title= fileName.split('\\image\\')[1].encode('utf-8'))
                self.latitude_list.append(gps[0])
                self.longitude_list.append(gps[1])


        gmap3.scatter(self.latitude_list, self.longitude_list, 'red',
                      size=60, marker=False)

        # Plot method Draw a line in
        # between given coordinates
        gmap3.plot(self.latitude_list, self.longitude_list,
                   'cornflowerblue', edge_width=2.5)
        gmap3.draw("maps.html")

    def getMap(self):
        os.system('start maps.html')

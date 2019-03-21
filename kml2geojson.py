#coding:utf-8
from fastkml import kml
from fastkml import geometry
from shapely.geometry import mapping
import json
#读取kml
class KMLDeal():
    #file：python打开的文件对象，在这里为文件路径
    def __init__(self,file):
        self.file=file
    #获取geometry的类型，用于组织geojson
    def getGeoType(self,geom):
        if isinstance(geom, geometry.Point):
            return "Point"
        elif isinstance(geom, geometry.LinearRing):
            return "LinearRing"
        elif isinstance(geom, geometry.LineString):
            return "LineString"
        elif isinstance(geom, geometry.Polygon):
            return "Polygon"
        elif isinstance(geom, geometry.MultiPoint):
            return "MultiPoint"
        elif isinstance(geom, geometry.MultiLineString):
            return "MultiLineString"
        elif isinstance(geom, geometry.MultiPolygon):
            return "MultiPolygon"
        elif isinstance(geom, geometry.GeometryCollection):
            return "GeometryCollection"
        else:
            raise ValueError("kml中包含无效的geometry类型.")
    #读取placemark属性
    def readPlaceMark(self,placemark):
        data=placemark.extended_data
        geom=placemark.geometry
        geoType=self.getGeoType(geom)
        properties={}
        for ele in data.elements:
            name=ele.name
            value=ele.value
            properties[name]=value
        result={
            "type": "Feature",
            "geometry": json.dumps(mapping(geom)),
            "properties": properties
        }
        return result
    #读取folder属性
    def readFolder(self,folder):
        folderresults=[]
        for placemark in folder.features():
            folderresults.append(self.readPlaceMark(placemark))
        return folderresults
    #读取kml的extenddata即属性和样式
    def getFeatureCollFromKml(self):
        file=self.file
        with open(file,'rt') as f:
            doc=f.read()
            # Create the KML object to store the parsed result
            k = kml.KML()
            # Read in the KML string
            k.from_string(doc)
            results=[]
            for doc in list(k.features()):
                if isinstance(doc,kml.Document):
                    for folder in list(doc.features()):
                        results.extend(self.readFolder(folder))
                elif isinstance(doc,kml.Folder):
                    results.extend(self.readFolder(doc))
                elif isinstance(doc,kml.Placemark):
                    results.extend(self.readPlaceMark(doc))
        FeatureCollection={ 
            "type": "FeatureCollection",
            "features":results
        }
        print(FeatureCollection)
        return FeatureCollection

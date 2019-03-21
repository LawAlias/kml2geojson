#coding:utf-8
from kml2geojson import KMLDeal

kmldeal=KMLDeal("kml.kml")
geojson=kmldeal.getFeatureCollFromKml()
print(geojson)
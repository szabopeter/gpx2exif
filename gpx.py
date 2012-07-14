#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom.minidom import parse, parseString
import time

def load(fn):
    pts = []
    doc = parse(fn)
    ltrkpt = doc.getElementsByTagName('trkpt')
    nr = 0
    for x in ltrkpt:
        lalt = x.getElementsByTagName('ele')
        alt = lalt[0].firstChild.data
        ltime = x.getElementsByTagName('time')
        if ltime == []:
            tme = -1
        else:
            nr+=1
            tme = ltime[0].firstChild.data
            tme = time.mktime(time.strptime(tme,"%Y-%m-%dT%H:%M:%SZ")) + 2*3600
            #print "%s,%s: %s"%( x.attributes["lat"].value, x.attributes["lon"].value, tme, )
        pts.append({ "lat" : float(x.attributes["lat"].value) ,
                         "lon" : float(x.attributes["lon"].value) ,
                         "tme" : tme ,
                         "alt" : float(alt) ,
                         "nr" : nr,
                         })
    return pts

def ptd(p1,p2):
    import math
    try:
        return 10000*math.hypot(p2['lat']-p1['lat'],p2['lon']-p1['lon'])
    except TypeError:
        return -1

if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        pts=load("test.gpx")
    else:
        pts=load(sys.argv[1])
    ex = None
    for x in pts:
        print "%03d %14.10f,%14.10f - %05.1f : %16s %5.2f"%(x['nr'],x["lat"],x["lon"],x["alt"],x["tme"],ptd(x,ex),)
        ex = x
    #print "%s trackpoints."%(len(pts),)

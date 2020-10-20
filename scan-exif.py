#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import EXIF
import gpx

if __name__ == '__main__':
    gpstoolpath = "/home/szp/app/Image-ExifTool-6.30/exiftool"
    if len(sys.argv) < 2:
        print("""
        Usage:
            setdif.py jpegtime gpstime (hh:mm:ss)
            scan-exif.py gpxfile.gpx jpeg1.jpg jpeg2.jpg ... jpegn.jpg >script.cmd
            . script.cmd

        Example:
            setdif.py 12:05:01 13:06:01
        """)
        sys.exit(1)
    f = open("setdif.dif", "r")
    dif = float(f.read().strip())
    f.close()
    pts = gpx.load(sys.argv[1])
    wpts = []
    for fn in sys.argv[2:]:
        f = open(fn, 'rb')
        tags = EXIF.process_file(f)
        f.close()
        try:
            tag = tags["EXIF DateTimeOriginal"]
            # print tag
            jpgt = time.mktime(time.strptime(
                str(tag), "%Y:%m:%d %H:%M:%S")) - dif
            l = 0
            u = len(pts)-1
            if pts[l]["tme"] <= jpgt and jpgt <= pts[u]["tme"]:
                while u-l > 1:
                    f = int((u+l)/2)
                    if jpgt < pts[f]["tme"]:
                        u = f
                    else:
                        l = f
                tl = pts[l]["tme"]
                tu = pts[u]["tme"]
                r = (jpgt - tl)/(tu-tl)
                lat = pts[l]["lat"]*(1-r)+pts[u]["lat"]*r
                lon = pts[l]["lon"]*(1-r)+pts[u]["lon"]*r
                alt = pts[l]["alt"]*(1-r)+pts[u]["alt"]*r
                wpts.append(f"""<wpt lat="%f" lon="%f">
    <ele>%f</ele>
    <name>%s</name>
    <cmt>%s</cmt>
    <desc>%s</desc>
    <sym>Flag, Blue</sym>
</wpt>""" % (lat, lon, alt, fn, tag, fn))
                latref, lonref = "N", "E"
                if (lat < 0):
                    latref = "S"
                if (lon < 0):
                    lonref = "W"
                lat, lon = abs(lat), abs(lon)
                print(gpstoolpath + """ -GPSLatitude=%s -GPSLatitudeRef=%s -GPSLongitude=%s -GPSLongitudeRef=%s -GPSAltitude=%f -GPSAltitudeRef=above "%s" """ % (
                    lat, latref, lon, lonref, alt, fn))
            else:
                sys.stderr.write("# Could not timeframe %s\n" % fn)
        except KeyError:
            sys.stderr.write("# No DateTimeOriginal tag found in %s\n" % fn)
    f = open("waypoints.gpx", "w")
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<gpx
    version="1.0"
    creator="GPSBabel - http://www.gpsbabel.org"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.topografix.com/GPX/1/0"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n""")
    f.write("\n".join(wpts))
    f.write("</gpx>\n")
    f.close()

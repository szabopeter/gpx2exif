#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    try:
        jpgts = sys.argv[1]
        gpsts = sys.argv[2]
        jpgtl = [int(x) for x in jpgts.split(":")]
        gpstl = [int(x) for x in gpsts.split(":")]
        jpgt = jpgtl[0] * 3600 + jpgtl[1] * 60 + jpgtl[0]
        gpst = gpstl[0] * 3600 + gpstl[1] * 60 + gpstl[0]
        dif = jpgt - gpst
        print(dif)
        with open("setdif.dif", "w") as f:
            f.write(f'{dif}\n')
    except IndexError:
        print("""
        Usage:
            setdif.py 12:34:56 12:43:56
                      jpeg     gps
        """)

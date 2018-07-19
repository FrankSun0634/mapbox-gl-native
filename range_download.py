#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function
from multiprocessing import Process
import urllib2
import math
import sys
import os
import gzip  
import StringIO  

# 主服务地址
host = 'http://www.baidu.com/dddxx'

def download_pbf(z,x,y):
    url = host + '{}/{}/{}.pbf'.format(z,x,y)
    try:
        path = './pbf/{}/{}'.format(z,x)
        if not os.path.exists(path):
            os.makedirs(path)
        res = urllib2.urlopen(url)
        body = res.read()
        data = StringIO.StringIO(body)
        unzip = gzip.GzipFile(fileobj = data)
        raw_data = unzip.read()
        unzip.close()
        filename = path + '/{}.pbf'.format(y)
        with open(filename,"wb") as fp:
            fp.write(raw_data)
            print('>', end='')

    except urllib2.HTTPError,e:
        if e.code != 404 and e.code != 400:
            print( '网络异常'.decode('UTF-8').encode('GBK'),e,url )   
    except IOError as e:
        print( '文件操作失败'.decode('UTF-8').encode('GBK'),e,url)
    except Exception as e:
        print( '错误 ：'.decode('UTF-8').encode('GBK'),e,url)

def spider(tile_lst=[]):
    for tile in tile_lst:
        download_pbf(tile[0],tile[1],tile[2])

def convert(x,y,l):
    x = (x + 180) / 360.0
    y = math.log( math.tan( (90 + y) * math.pi / 360)) / (math.pi / 180)
    y = (1 - y / 180.0) / 2.0
    return (int(math.floor(x * math.pow(2.0,l))),
        int(math.floor(y * math.pow(2.0,l))))


if __name__ == '__main__':
    # l0 = int(sys.argv[1])
    # x0 = int(sys.argv[2])
    # y0 = int(sys.argv[3])
    minx = 73
    maxx = 135
    miny = 0
    maxy = 53
    l0 = 0 
    l1 = 6
    # 瓦片地址数组
    tile_lst = []
    for lvl in range(l0, l1 + 1):
        lu = convert(minx, maxy, lvl)
        rd = convert(maxx, miny, lvl)
        for x in range(lu[0], rd[0]):
            for y in range(lu[1], rd[1]):
                tile_lst.append((lvl,x,y))

    if len(tile_lst) < 30:
        for val in tile_lst:
            download_pbf(val[0],val[1],val[2])
    else:
        step = int(len(tile_lst) / 10)
        for i in range(0,9):
            start = i*step
            end = (i+1)*step
            p = Process(target=spider, args=(tile_lst[start:end],))
            p.start()
        start = 9*step
        end = len(tile_lst)
        p = Process(target=spider, args=(tile_lst[start:end],))
        p.start()

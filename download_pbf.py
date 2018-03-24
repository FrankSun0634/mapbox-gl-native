#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from multiprocessing import Process
import urllib2
import math
import sys
import os


# token 池
token = [
'pk.eyJ1IjoiZ2FyeWh1IiwiYSI6ImNqZWYwdDF5aDFjODkzM28ycTBvMjM4NWsifQ.JU9SXOvw99tVm7fXxL4MrQ',
'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA',
'pk.eyJ1IjoiZmFudmFuemgiLCJhIjoiY2l0ZmRsaHg4MDliNDJvbXk5NXBvdTM2NCJ9.CBkukvDUouPK6DN2gECEJQ',
'pk.eyJ1IjoienhxaW4yeW91bmciLCJhIjoiY2pmM2xkbHM0MTVveDMxazd6dzB0bHQ3MCJ9.vUo44am_Gu3YH5u-fmLLDw',
'pk.eyJ1IjoiZXhsaW1pdCIsImEiOiJjamV4dGZwcTkwN2VpMzNsbmozbTlicDliIn0.JJEnXHsW-4QalDXMNfKdzw'
]
# 主服务地址
host = 'https://b.tiles.mapbox.com/v4/mapbox.mapbox-terrain-v2,mapbox.mapbox-streets-v7/'


def save_img(img_url,file_name,file_path='./pbf'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        file_path = "./pbf/" + file_name
        last_off = file_path.rfind('/')
        file_path = file_path[0: last_off]
        #print "file-path: " + file_path
        if not os.path.exists(file_path):
            print '文件夹',file_path,'不存在，重新建立'
            #os.mkdir(file_path)
            os.makedirs(file_path)

        #拼接图片名（包含路径）
        #filename = '{}{}{}'.format(file_path,os.path.sep,file_name)
        filename = "./pbf/" + file_name
        print "filename : " + filename
        #print "file name is : " + filename
        #下载图片，并保存到文件夹中
        response = urllib2.urlopen(img_url, timeout=30)
        cat_img = response.read()
        with open(filename, 'wb') as f:
            f.write(cat_img)
    except IOError as e:
        print '文件操作失败',e
        return False
    except Exception as e:
        print '错误 ：',e
        return False
    return True
    
def spider(l0,x0,y0):
    token_idx = 0
    # 上一次停止的地方
    width   = pow(2.0, l0)
    x_min   = x0 / width
    x_max   = (x0 + 1) / width
    y_min   = y0 / width
    y_max   = (y0 + 1) / width
    start_l = l0
    start_x = 0
    start_y = 0
    try:
        filename = './pbf/break-{}_{}_{}.txt'.format(l0,x0,y0)
        with open(filename) as f:
            break_str = f.read()
            last = break_str.split(',')
            if len(last) >= 3:
                start_l = int(last[0])
                start_x = int(last[1])
                start_y = int(last[2])
    except Exception:
        print filename + " missing"

    # 开始工作啦
    for lvl in range(start_l,18):
        # 如果过了断开的那一层，恢复 xy
        width = int(math.pow(2,lvl))
        minx = int(x_min * width)
        maxx = int(x_max * width)
        miny = int(y_min * width)
        maxy = int(y_max * width)
        if lvl > start_l: 
            start_x = minx
            start_y = miny
        for x in range(minx,maxx):
            # 如果过了断开的那一列，恢复y
            if x > start_x: 
                start_y = miny;
            for y in range(miny,maxy):
                #6/15/24.vector.pbf        
                path = str(lvl) + '/' + str(x) + '/' + str(y) + '.vector.pbf'
                url_path = host + path + '?access_token=' + token[token_idx]
                while not save_img(url_path, path):
                    token_idx += 1
                    if token_idx >= len(token):
                        filename = './pbf/break-{}_{}_{}.txt'.format(l0,x0,y0)
                        f = open(filename,'w')
                        f.write('{},{},{}'.format(lvl,x,y))
                        f.close()
                        return
                    url_path = host + path + '?access_token=' + token[token_idx]

def loop_down(l,x,y):
    while True:
        spider(l,x,y)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "please input : down.py l x y"
        sys.exit(0)
    l0 = int(sys.argv[1])
    x0 = int(sys.argv[2])
    y0 = int(sys.argv[3])
    for x in range(x0, x0 + 5):
        for y in range(y0, y0 + 5):
            p = Process(target=loop_down, args=(l0,x,y))
            p.start()
            #p.join() #串行


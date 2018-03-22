#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import urllib2
import math
import os

def save_img(img_url,file_name,file_path='./pbf'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        file_path = "./pbf/" + file_name
        last_off = file_path.rfind('/')
        file_path = file_path[0: last_off]
        print "file-path: " + file_path
        if not os.path.exists(file_path):
            print '文件夹',file_path,'不存在，重新建立'
            #os.mkdir(file_path)
            os.makedirs(file_path)

        #拼接图片名（包含路径）
        #filename = '{}{}{}'.format(file_path,os.path.sep,file_name)
        filename = "./pbf/" + file_name
        print "filename is : " + filename
        #print "file name is : " + filename
        #下载图片，并保存到文件夹中
        response = urllib2.urlopen(img_url)
        cat_img = response.read()
        with open(filename, 'wb') as f:
            f.write(cat_img)
    except IOError as e:
        print '文件操作失败',e
    except Exception as e:
        print '错误 ：',e
        return False
    return True
# token 池
token = [
'pk.eyJ1IjoiZ2FyeWh1IiwiYSI6ImNqZWYwdDF5aDFjODkzM28ycTBvMjM4NWsifQ.JU9SXOvw99tVm7fXxL4MrQ',
'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA',
'pk.eyJ1IjoiZmFudmFuemgiLCJhIjoiY2l0ZmRsaHg4MDliNDJvbXk5NXBvdTM2NCJ9.CBkukvDUouPK6DN2gECEJQ'
]
# 主服务地址
host = 'https://b.tiles.mapbox.com/v4/mapbox.mapbox-terrain-v2,mapbox.mapbox-streets-v7/'
token_idx = 0
# 上一次停止的地方
start_l = 5
start_y = 31
start_x = 11
# 开始工作啦
for lvl in range(start_l,10):
    # 如果过了断开的那一层，恢复 xy
    if lvl > start_l: 
        start_x = 0
        start_y = 0
    maxx = int(math.pow(2,lvl))
    for x in range(start_x,maxx):
        # 如果过了断开的那一列，恢复y
        if x > start_x: 
            start_y = 0;
        for y in range(start_y,maxx):
            #6/15/24.vector.pbf        
            path = str(lvl) + '/' + str(y) + '/' + str(x) + '.vector.pbf'
            url_path = host + path + '?access_token=' + token[token_idx]
            while not save_img(url_path, path):
                token_idx += 1
                url_path = host + path + '?access_token=' + token[token_idx]
                if token_idx >= len(token):
                    os._exit(0)

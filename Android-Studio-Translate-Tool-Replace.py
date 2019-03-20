# -*- coding:utf-8 -*-
from __future__ import print_function
import zipfile
import os
import shutil
import time
import property
import shutil

print('====================================\n\nThis Software Only For Android Studio Language Package Replace\nDevelop By Wellchang\n2019/03/20\n\n====================================\n\n')

print('please input the absolute path of new resource_en.jar file',end=':')
filename = input()
print('please input the absolute path of old resource_en.jar file',end=':')
filename_cn = input()
splitNew = filename.split('.')
splitLen = len(splitNew)
prefix = splitNew[splitLen-1]
prefixWithDot = '.' + splitNew[splitLen-1]
path2 = filename.replace(prefixWithDot,'')
path2_cn = filename_cn.replace(prefixWithDot,'')

print('Decompression new resource_en.jar file...',end='',flush=True)
fz = zipfile.ZipFile(filename, 'r')
for file in fz.namelist():
    # print(file)
    fz.extract(file, path2)
print('Done')

print('Decompression old resource_en.jar file...',end='',flush=True)
fzo = zipfile.ZipFile(filename_cn, 'r')
for file in fzo.namelist():
    # print(file)
    fzo.extract(file, path2_cn)
print('Done')

print('translate new resource_en.jar file...',end='',flush=True)
for file in fz.namelist():
    if(file.endswith(".properties")):
        props = property.parse(path2 + '\\' + file)
        keys = props.keys
        for fileCN in fzo.namelist():
          if(fileCN == file):
            propsCN = property.parse(path2_cn + '\\' + file)
            keysCN = propsCN.keys
            for key in keys:
              # print(len(keys))
              # print(file + "=======>" + key + "=" + props.get(key))
              if(propsCN.has_key(key)):
                props.set(key,propsCN.get(key))
        props.save()
        keys.clear()
print('Done')

print('Packing Translated file...',end='',flush=True)
file_new = path2 + "_new.jar"
zNew = zipfile.ZipFile(file_new, 'w', zipfile.ZIP_DEFLATED)
for dirpath, dirnames, filenames in os.walk(path2):  # os.walk 遍历目录
    fpath = dirpath.replace(path2, '')   # 这一句很重要，不replace的话，就从根目录开始复制
    fpath = fpath and fpath + os.sep or ''  # os.sep路径分隔符
    for filename in filenames:
        zNew.write(os.path.join(dirpath, filename), fpath+filename)
        # os.path.join()函数用于路径拼接文件路径。
        # os.path.split(path)把path分为目录和文件两个部分，以列表返回
print('Done')
zNew.close()
print('Delete the extracted file...',end='',flush=True)
shutil.rmtree(path2)
shutil.rmtree(path2_cn)
print('Done')
print('Translation completed!!!')

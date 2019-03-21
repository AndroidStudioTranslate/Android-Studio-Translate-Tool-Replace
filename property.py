#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import os
import tempfile


class Properties:
    values = []
    keys = []

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
                    self.keys.append(strs[0].strip())
                    self.values.append(strs[1].strip())
        except Exception as e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return self.properties.get(key, None) != None

    def get(self, key, default_value=''):
        if self.properties.get(key, None) != None:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key +
                         '=' + value.replace("\\", "\\\\"), True)

    def set(self, key, value):
        self.properties[key] = value
    
    def save(self):
        content = ''
        for k,v in self.properties.items():
            content = content + k + "=" + v + "\n"
        content = content.strip('\n')
        s_open = open(self.file_name, 'w')
        s_open.write(content)  # 将内容写入原文件
        s_open.close()

def parse(file_name):
    return Properties(file_name)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    file = tempfile.TemporaryFile()  # 创建临时文件

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:  # 读取原文件
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            file.write(line.encode("utf-8"))  # 写入临时文件
        if not found and append_on_not_exists:
            file.write(('\n' + to_str).encode("utf-8"))
        r_open.close()
        file.seek(0)

        content = file.read()  # 读取临时文件中的所有内容

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content.decode("utf-8"))  # 将临时文件中的内容写入原文件
        w_open.close()

        file.close()  # 关闭临时文件，同时也会自动删掉临时文件
    else:
        print("file %s not found" % file_name)

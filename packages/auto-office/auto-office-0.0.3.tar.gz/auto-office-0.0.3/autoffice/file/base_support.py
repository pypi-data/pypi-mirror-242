'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/7 16:38
@File_name: base_support.py
'''

import os
import re
import stat

import imghdr
import shutil

# 图片识别模块中通过后缀名识别图片
IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG','.png', '.PNG',
    '.ppm', '.PPM', '.bmp', '.BMP', '.tiff'
]

'''---------------------------------------------------------------------------------'''
def is_image(file_path):
    '''
    判断指定文件是否为图片

    Args:
        file_path: str, 文件绝对路径
    '''
    return imghdr.what(file_path) in IMG_EXTENSIONS


def delete(path):
    '''
    删除文件夹或文件

    Args:
        path: str, 文件或文件夹绝对路径
    '''

    if os.path.isdir(path):
        # 如果对应路径为文件夹
        def remove_readonly(func, path, _):           # 错误回调函数，改变只读属性位，重新删除
            "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(path, onerror=remove_readonly)  # 设置错误回调函数οnerrοr

    elif os.path.isfile(path):
        # 如果对应路径为文件
        if not os.access(path, os.W_OK):
            # 如果文件没有写入权限
            os.chmod(path, stat.S_IWUSR)
        os.remove(path)


def file_in_folder(folder_path):
    '''
    在给定主文件夹下，找出包括子文件夹内文件在内的所有的非文件夹文件

    Args:
        folder_path: 文件夹路径
    return:
        file_path_list: 非文件夹文件绝对路径的列表
    '''

    file_path_list = []
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isdir(file_path):            # 判断是否为文件夹
                file_path_list.extend(file_in_folder(file_path))
            else:
                file_path_list.append(file_path)    # 当判断出这不是文件夹, 而是文件时, 将路径加到list中
    else:
        print('注意, 路径并不对应一个文件夹:\n{}'.format(folder_path))

    return file_path_list


def dissolution_folder(folder_path):
    '''解散指定的文件夹'''

    if os.path.isdir(folder_path):    # 判断是否为文件夹
        parent_folder_path = os.path.dirname(folder_path)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            tar_path = os.path.join(parent_folder_path, file)
            shutil.move(file_path, tar_path)

        delete(folder_path)
    else:
        print("指定路径非文件夹, 无法解散")


def str_is_number(string):
    '''
    判断一个字符串是否为数值, 可识别百分数

    [-+]? 表示可选的正负号
    [0-9,]* 表示零个或多个数字, 逗号应对可能的会计数字
    \.? 表示可选的小数点
    [0-9]* 表示零个或多个数字
    ([eE][-+]?[0-9]+)? 表示可选的科学计数法表示
    [%]?表示可选的%号
    '''

    pattern = re.compile(r'^[-+]?[0-9,]*\.?[0-9]*([eE][-+]?[0-9]+)?[%]?$')
    return bool(pattern.match(string))


def is_all_chinese(strs):
    '''检验是否全是中文字符'''

    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def is_contains_chinese(strs):
    '''检测时否有中文字符'''
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def is_all_english(strs):
    '''检测是否全是英文字符'''
    import string
    for i in strs:
        if i not in string.ascii_lowercase + string.ascii_uppercase:
            return False
    return True


def is_contains_english(strs):
    '''检测是否含有英文字符'''
    pattern = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(pattern, strs)
    if len(res):
        return True
    else:
        return False
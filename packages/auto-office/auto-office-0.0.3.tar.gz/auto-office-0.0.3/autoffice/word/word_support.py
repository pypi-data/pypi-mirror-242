'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/21 10:41
@File_name: word_support.py
'''

import os
from tqdm import tqdm
from win32com.client import Dispatch
from ..file.base_support import *

def word2pdf(word_path, remove=True):
    '''
    将单个word文件转化为pdf文件

    Args:
        word_path: str, 目标word的绝对路径
        remove: boolean, pdf转换完成后, 是否删除原word, 默认为是
    '''

    wdFormatPDF = 17  # win32提供了多种word转换为其他文件的接口，其中FileFormat=17是转换为pdf
    word = Dispatch('Word.Application')

    try:
        doc = word.Documents.Open(word_path)
    except Exception as e:
        print("word无法打开, 发生如下错误:\n{}".format(e))
        word.Quit()

    try:
        pdf_file_name = word_path.replace(".docx", ".pdf").replace(".doc", ".pdf")
        pdf_file = os.path.join(os.path.dirname(word_path), pdf_file_name)
        doc.SaveAs(pdf_file, FileFormat = wdFormatPDF)
        doc.Close()
        if remove:
            delete(word_path)
    except Exception as e:
        print("文件保存失败, 发生如下错误:\n{}".format(e))
        word.Quit()

    word.Quit()

def words2pdf(word_path_list, remove=True):
    '''
    将指定路径集合中的word文件转为pdf
    Args:
        word_path_list: list, word文件的路径列表
        remove: boolean, 是否保留原有的word文件
    '''

    word_path_list = [file_path for file_path in word_path_list
                           if file_path.endswith(".docx") or file_path.endswith(".doc")]

    for file_path in tqdm(word_path_list, desc='word转换进度: ', colour='BLACK', leave=False):
        word2pdf(file_path, remove=remove)
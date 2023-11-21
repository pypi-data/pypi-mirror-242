'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/17 15:45
@File_name: pdf_function.py
'''

import os
from collections import Iterable
from tqdm import tqdm
from PyPDF2 import PdfWriter, PdfReader
from .pdf_support import *


def extract_pdf(pdf_path, page_list, save_posit=None):
    """
    提取pdf文件中指定页数的部分, 并创建新文件

    Args:
        pdf_path: str, 文件路径
        page_list: list, 需要提取的pdf页面list(从1开始而不是0), 其中元素可为整数或可迭代类型(例如[1,6,10], (2,5,7))
        save_posit: str, 提取的pdf页面新文件要保存的目录, 默认为pdf对应目录
    """

    folder_path, pdf = os.path.split(pdf_path)        # 划分为文件头和pdf文件本身
    pdf_name, pdf_extension = os.path.splitext(pdf)   # 将pdf本身划分为文件名和拓展名

    save_posit = os.path.dirname(pdf_path) if save_posit is None else save_posit
    if not os.path.exists(save_posit):
        os.mkdir(save_posit)
    pdf_reader = PdfReader(pdf_path)

    # 读取每一页的数据
    for pages in page_list:
        pdf_writer = PdfWriter()
        if isinstance(pages, Iterable):
            for page in pages:
                pdf_writer.add_page(pdf_reader.pages[page-1])
            index = '{}-{}'.format(pages[0], pages[-1])
        elif isinstance(pages, int):
            pdf_writer.add_page(pdf_reader.pages[pages-1])
            index = str(pages)
        else:
            print("\"{}\"表述有误, 应为可迭代对象或整数".format(pages))

        # 保存提取的文件
        save_path = os.path.join(save_posit, pdf_name + '_' + index + '.pdf')
        with open(save_path, "wb") as out:
            pdf_writer.write(out)

    print("文件已成功提取，保存路径为: " + save_posit)


def corres_pdfs_merge(pdf_folder1, pdf_folder2, df, save_posit, order = 1, name='pre'):
    '''
    将两个文件夹中的pdf群, 按照dataframe中的对应顺序, 进行合并

    Args:
        pdf_folder1: str, 装有pdf文件的文件夹1绝对路径, 默认在合并后居前
        pdf_folder2: str, 装有pdf文件的文件夹2绝对路径, 默认在合并后居后
        df: pandas.Dataframe, 第一、二列分别对应两个pdf文件夹中的文件如何对应合并, 内容为文件名+拓展名
        save_posit: str, 提取的pdf页面新文件要保存的目录, 默认为pdf对应目录
        order: int, 文件合并顺序, 默认为1, 即pdf_folder1在合并后居前, pdf_folder2居后
        name: str, 文件命名顺序, 默认为'pre', 即用pdf_folder1中文件命名合并后pdf
    '''

    df.set_index(df.columns[0], inplace=True)
    for pdf1 in tqdm(os.listdir(pdf_folder1)):
        pdf1_path = os.path.join(pdf_folder1, pdf1)
        pdf2 = df.loc[pdf1, df.columns[0]]
        pdf2_path = os.path.join(pdf_folder2, pdf2)

        file_name = pdf1 if name == 'pre' else pdf2
        out_path = os.path.join(save_posit, file_name)
        pdf_order = [pdf1_path, pdf2_path] if order == 1 else [pdf2_path, pdf1_path]
        merge_pdfs_from_paths(pdf_order, out_path)
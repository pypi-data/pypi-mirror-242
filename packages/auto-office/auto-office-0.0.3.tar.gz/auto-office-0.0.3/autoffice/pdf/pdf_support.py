'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/17 15:38
@File_name: pdf_support.py
'''

import os
import shutil
from tqdm import tqdm
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from PyPDF2 import PdfWriter, PdfReader
from ..file.base_support import *
import pandas as pd

def merge_pdfs_from_paths(pdf_path_list, save_posit, merge_name='合并.pdf'):
    '''
    将指定路径集合中的文件合并为一个pdf, 并保存至相应路径下

    Args:
        pdf_path_list: list, 待合并的pdf文件的绝对路径集合, 可仅有一个pdf文件, 此时为功能退化为文件移动
        save_posit: str, 合并后文件的保存文件夹绝对地址
        merge_name: str, 合并后的文件命名, 默认为'合并.pdf'
    '''

    if len(pdf_path_list) > 1:
        pdf_writer = PdfWriter()
        for path in pdf_path_list:
            pdf_reader = PdfReader(path)
            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])
        out_put = os.path.join(save_posit, merge_name)
        with open(out_put, 'wb') as out:
            pdf_writer.write(out)
    elif len(pdf_path_list) == 1:
        shutil.move(pdf_path_list[0], os.path.join(save_posit, merge_name))
    else:
        pass


def merge_pdfs_from_folder(folder_path, save_posit=None, merge_name='合并.pdf'):
    '''
    将指定文件夹下的所有pdf文件合并为一个文件

    Args:
        folder_path: str, 指定文件夹的绝对路径
        save_posit: str, 合并后文件的保存文件夹绝对地址, 默认为None, 即合并pdf默认保存在原文件夹处
        merge_name: str, 合并后的文件命名, 默认为'合并.pdf'
    '''

    if save_posit is None:
        save_posit = folder_path
    paths = []
    for file in os.listdir(folder_path):
        if file.endswith('.pdf') or file.endswith('.PDF'):
            paths.append(os.path.join(folder_path, file))

    merge_pdfs_from_paths(paths, save_posit, merge_name)


def imgs2pdf(file_path_list, save_posit=None, pagesize=A4, remove=True):
    '''
    将指定路径下的图片文件转为pdf

    Args:
        file_path_list: 图片的路径列表
        save_posit: str, 转换后pdf的保存文件夹绝对地址, 默认为None, 即转换后pdf默认保存在原图片处
        pagesize: tuple, 预定义好的元组, 可选A4、A3等常见大小, 默认为A4, 也可自行定义
        remove: 是否保留原有的图片文件, 默认保留
    '''

    img_path_list = [file_path for file_path in file_path_list if is_image(file_path)]
    for img_path in tqdm(img_path_list, desc='图片转换进度: ', colour='BLACK', leave=False):
        if save_posit is not None:
            file_name = os.path.split(img_path)[1]
            pdf_name = os.path.splitext(file_name)[0] + '.pdf'
            pdf_path = os.path.join(save_posit, pdf_name)
        else:
            pdf_path = None
        img2pdf(img_path, pdf_path=pdf_path, pagesize=pagesize, remove=remove)


def img2pdf(img_path, pdf_path=None, pagesize=A4, remove=True):
    """
    将指定路径的图片转成PDF文件, 默认转化为竖版A4大小
    Args:
        img_path: str, 图片的路径
        pdf_path: str, 要保存的PDF文件的路径, 默认为None, 即保留在图片原位置
        pagesize: tuple, 预定义好的元组, 可选A4、A3等常见大小, 默认为A4, 也可自行定义
        remove: bool, 转为pdf后是否删除原图片, 默认为True
    """
    # 打开指定路径的图片
    img = Image.open(img_path)
    width, height = img.size

    # 创建空白PDF文件, 根据图片长宽确定是竖版还是横板
    pagesize = pagesize if width <= height else landscape(pagesize)
    pdf_path = os.path.splitext(img_path)[0] + '.pdf' if pdf_path is None else pdf_path
    c = canvas.Canvas(pdf_path, pagesize=pagesize)

    # 计算缩放/扩大比例, 这一步使用了短板效应原则
    width_scale= pagesize[0] / width
    height_scale = pagesize[1] / height
    scale = min(width_scale, height_scale)
    size = (int(width * scale), int(height * scale))
    img = img.resize(size)
    width, height = img.size


    # 将图像绘制在PDF页面上
    c.drawImage(img_path, (pagesize[0] - width) / 2, (pagesize[1] - height) / 2, width, height)
    c.save()
    if remove:
        delete(img_path)
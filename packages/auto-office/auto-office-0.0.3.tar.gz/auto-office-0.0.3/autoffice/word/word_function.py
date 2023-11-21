'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/7/24 14:52
@File_name: word_function.py
'''

from ..excel.adjust import excel_format_adj
import os
import cpca
from tqdm import tqdm
import pandas as pd
from docxtpl import DocxTemplate


def address_sep(excel_path, sheet=1, address_col='地址', out_path='标准化地址.xlsx'):
    '''
    将excel中长串字符串地址转化为标准化地址省、市、区, 可用于投行函证工作

    Args:
        excel_path: str, 存放地址的excel文件绝对路径
        sheet: int, 路径存放在第几张表, 从1开始
        address_col: str, 路径存放在哪一列
        out_path: str, 输出位置, 默认为'标准化地址.xlsx'
    '''

    df = pd.read_excel(excel_path, sheet_name=sheet-1)
    address_list = df[address_col].to_list()
    std_address = cpca.transform(address_list)

    std_address.to_excel(out_path, sheet_name='标准化地址', index=True)
    excel_format_adj(out_path, first_line=True)


def generate_Word_from_tpl(tpl, keywords, sheet=1, files=False):
    '''
    根据模板替换关键词批量生成word文件并存放到指定位置

    Args:
        tpl: str, 模板word文件所在的路径
        keywords: str, 关键词excel文件所在的路径
        sheet: int, 关键词放在哪张表中, 从1开始计数
        files: boolean, 当files为Trues时, 创建word文件前会创建一个同名文件夹, word在其中
    '''

    # 在模板文件的同文件夹下新建文件夹用于存放批量生成的word
    folder_path = os.path.join(os.path.dirname(tpl), r'生成文件存放位置')
    if not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)  # 创建一级目录
        except:
            print('创建文件夹失败, 请检查权限问题')
            return False

    df = pd.read_excel(keywords, sheet_name=sheet-1)
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        context = {col_label: value for col_label, value in zip(row.index, row.str.strip().values)}
        tpl_word = DocxTemplate(tpl)
        tpl_word.render(context)  # 渲染替换
        if files:
            word_path = os.path.join(folder_path, row[0])
            os.mkdir(word_path)
            tpl_word.save(os.path.join(word_path, r'{}.docx'.format(row[0])))
        else:
            tpl_word.save(os.path.join(folder_path, r'{}.docx'.format(row[0])))
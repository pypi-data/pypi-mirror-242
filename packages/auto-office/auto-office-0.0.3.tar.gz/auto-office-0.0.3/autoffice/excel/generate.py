'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/17 15:35
@File_name: generate.py
'''
import os.path
import time
import pandas as pd
import tabula
import camelot.io as camelot


def get_pdf_table(
    file, pages: str,
    multiple_tables=True,
    mode="stream",
    area=None,
    relative_area=False,
    encoding='gbk',
    password=None,
    engine='tabula'
):
    """
    导出pdf指定页面的表格, 并结合人工判断完成微调

    Args:
        file: str, 要读取表格的pdf文件路径
        pages: 字符串或列表, 表格所在pdf的页数。举例: '1-7,10', 'all', [1,2]
        multiple_tables: boolean, 是否将多个表格合一输出, True为分开输出, False为合并输出
        mode: str, 模式选择,
              lattice: 利用 ghostscript 将PDF页面转换为图像, 再用OpenCV进行处理
              stream: PDFMiner使用margin解析单元格之间有空格的表格以模拟表格
        area: list, 指定表格坐标, 初次运行的时候可以给的不那么精细, 坐标为[上, 左, 下, 右], 举例[10,0,80,100]
        relative_area: boolean, 百分比坐标模式, 当为True时area参数应输入百分比参数
        encoding: str, 编码格式, 一般gbk就可以了, 有问题的话可以试试utf-8
        password: 如果pdf文件有密码, 需要把密码输入该参数
        engine: str, 使用何种引擎进行识别, 可选tabula或cameplot, 目前cameplot未开发完成

    return:
        tables: 返回一个由dataframe构成的列表list
    """

    if engine == 'tabula':
        final_tables = []
        mode = True if mode == "stream" else False

        # 这一步的作用是保留输入页码, 方便后续给用户定位可能有问题的表格的页码, 输入为all的情况下不行
        if isinstance(pages, str) and pages != "all":
            list_num = pages.split(',')
        else:
            list_num = pages
        tables = tabula.read_pdf(
            file, pages=pages,
            multiple_tables=multiple_tables,
            stream=mode,
            lattice=not mode,
            area=area,           # 上, 左, 下, 右
            relative_area=relative_area,  # 百分比坐标
            encoding=encoding,
            password=password
        )

        print('------------------初步识别出{}张表格------------------\n'.format(len(tables)))
        for i in range(len(tables)):
            if pages != "all":
                print("表格{}展示, 它大约在PDF文件的第{}页\n".format(i + 1, list_num[i]))
            time.sleep(1)
            print(tables[i])
            res = bool(int(input("\n该表格识别效果如何? 如果你认为可以, 输入1, 它将被记入最终输出, 否则输入0执行错误流程: ")))
            if res:
                final_tables.append(tables[i])
            else:
                print("\n-------执行错误处理流程-------")
                if pages != "all":
                    print("这张可能识别有误的表格大约在PDF文件的第{}页左右, 请再次自行判断".format(list_num[i]))
                flag = bool(int(input("是否再次识别?(1/0): ")))
                page_new = int(input('请输入识别有误的表格对应真实页码: '))
                while flag:
                    area_new = list(map(
                        float,
                        input('先前识别有误的原因可能是位置参数area不妥, 请在此输入一个包含四个位置的字符, 用逗号分隔: ').split(',')
                    ))
                    table = tabula.read_pdf(
                        file, pages=page_new,
                        multiple_tables=multiple_tables,
                        stream=mode,
                        area=area_new,
                        relative_area=relative_area,
                        encoding=encoding,
                        password=password
                    )
                    print("\n再次识别的表格{}展示\n".format(i+1))
                    print(table)
                    flag = bool(int(input("\n该表格识别效果如何? 是否再次识别?(1/0): ")))
                    if not flag:
                        final_tables.append(tables[i])
            print('\n------------------------------------------------------------------------')

        return tables

    # if engine == 'cameplot':
    #     tables = camelot.read_pdf(
    #         file, pages=pages,
    #         flavor=mode,
    #         table_areas=area,
    #         flage_size=True,       # 是否识别上（下）标文字
    #         process_background=process_background,  # 背景线是否隐藏在图片中
    #         password=password,
    #     )
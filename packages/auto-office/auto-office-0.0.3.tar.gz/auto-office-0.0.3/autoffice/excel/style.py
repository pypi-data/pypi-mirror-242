'''
-*- coding:utf-8
@Author: GYH
@Software: PyCharm
@Time: 2023/11/7 16:46
@File_name: style.py
'''


from openpyxl.styles import Font, Border, Side, Alignment

# excel格式调整中的最大行数
MAX_ROWS = 300

'''--------------这一部分内置了许多可以供全局调用的openpyxl样式--------------'''
'''边框'''
# 四方黑框, 经典款
border_norm = Border(
    left=Side(border_style='thin', color='000000'),
    right=Side(border_style='thin', color='000000'),
    top=Side(border_style='thin', color='000000'),
    bottom=Side(border_style='thin', color='000000'),
)
# 下框线, 用于三线表或首行表头分隔
border_first_row = Border(bottom=Side(border_style='medium', color='000000'))

'''对齐'''
# 经典样式: 四方居中, 无缩进、倾斜, 具有自动换行
alignment_norm = Alignment(
    horizontal='center', vertical='center',
    text_rotation=0,
    wrap_text=True,  # 自动换行
    indent=0  # 缩进
)
# 数字样式: 居中靠右, 自动换行
alignment_num = Alignment(horizontal='right', vertical='center', wrap_text=True)

'''字体'''
# 中文经典样式: 11号字微软雅黑不加粗, 非斜体, 黑色
font_cn = Font(
    name='微软雅黑',
    size=11, bold=False,
    italic=False, strike=False,
    color='000000'
)
# 英文经典样式: 11号字Calibri不加粗, 非斜体, 黑色
font_en = Font(
    name='Calibri',
    size=11, bold=False,
    italic=False, strike=False,
    color='000000'
)
# 特殊标注英文、数字字体: 11号字Calibri不加粗, 斜体, 海蓝色
font_blue = Font(name='Calibri', size=11, italic=True, color='0070C0')  # yoy表头字体
# 负数特殊标注: 11号字Calibri不加粗, 斜体, 红色
font_red = Font(name='Calibri', size=11, color='FF0000')

'''------------------------------------------------------'''
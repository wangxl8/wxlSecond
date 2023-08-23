import logging
from logging import handlers
import datetime
import os  # 导入获取路径
import random
import string
import time  # 导入时间格式

import ddddocr
from PIL import Image

from selenium.webdriver.common.by import By
import xlrd


# 获取验证码的函数
def get_code(driver, id):

    # 获取屏幕截图
    t = time.strftime('%Y%m%d_%H%M%S')    # 获取以时间命名的截图名称
    path = os.path.dirname(os.path.dirname(__file__)) + '\\screenshots'
    pic_name1 = path + '\\' + str(t) + '.png'

    driver.save_screenshot(pic_name1)    # 截取全屏

    # 抠出验证码区域
    captcha = driver.find_element(By.ID, id)  # 找到验证码区域

    left = captcha.location['x']   # 找到其左顶点坐标，并获取其高度和宽度
    top = captcha.location['y']
    right = left + captcha.size['width']
    height = top + captcha.size['height']

    # 保险方法，获取分辨率的系数，抠图时乘以相关系数
    dpr = driver.execute_script('return window.devicePixelRatio')
    # 开始在第一张图片里进行抠图
    im = Image.open(pic_name1)
    img = im.crop((left*dpr, top*dpr, right*dpr, height*dpr))
    # 定义抠图名称
    t = time.strftime('%Y%m%d_%H%M%S')
    pic_name2 = path + '\\' + str(t) + '.png'
    # 保存抠图
    img.save(pic_name2)
    # 使用ocr接口输出验证码字符，获取途中验证码字符串并返回
    ocr = ddddocr.DdddOcr()
    with open(pic_name2, 'rb') as f:
        img_data = f.read()
    ret = ocr.classification(img_data)
    # 返回验证码字符
    return ret


# 生成随机字符串的函数
def get_random_str():
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


# 定义和获取日志的函数
def get_logger():
    # 设置一个名为'mylogger'的logger
    logger = logging.getLogger('mylogger')
    # 设置logger的级别为DEBUG
    logger.setLevel(logging.DEBUG)
    path = os.path.dirname(os.path.dirname(__file__)) + '\\logs'

    # 设置一个handler，按照时间切割，文件名为all.log，when是开始时间，interval是间隔时间，backupcount是备份数量，attime是具体的时间
    # 设置好了时候，程序就会按照时间点进行拆分日志
    a_log = path + '\\' + 'all.log'
    rf_handler = logging.handlers.TimedRotatingFileHandler(a_log, when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0))
    # 设置日志的格式
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 日志估计较少，只在一个文件里存储
    e_log = path + '\\' + 'error.log'
    f_handler = logging.FileHandler(e_log)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s'))

    # 在新增handler时判断是否为空，如果为空，把handler对象加到logger里，解决日志重复输出问题
    if not logger.handlers:
        logger.addHandler(rf_handler)
        logger.addHandler(f_handler)
    # logger.addHandler(rf_handler)
    # logger.addHandler(f_handler)

    return logger


# 一行一行获取excel数据的函数
def get_excel_rowdata(filepath, sheetname):
    read_excel = xlrd.open_workbook(filepath)
    sheet = read_excel.sheet_by_name(sheetname)
    rows = sheet.nrows
    lst = []
    for row in range(rows):
        row_date = sheet.row_values(row)
        lst.append(row_date)
    return lst

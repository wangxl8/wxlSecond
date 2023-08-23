from selenium.webdriver.support.select import Select
from util import util


class BasePage(object):
    # 初始化一个driver
    def __init__(self, driver):
        self.driver = driver
        self.logger = util.get_logger()

    # 获取元素定位
    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    # 输入文本
    def type_text(self, text, *loc):
        self.find_element(*loc).send_keys(text)

    # 根据下拉框文本进行选择
    def select(self, text, *loc):
        elem = self.find_element(*loc)
        Select(elem).select_by_visible_text(text)

    # 点击事件
    def click(self, *loc):
        self.find_element(*loc).click()

    # 清除
    def clear(self, *loc):
        self.find_element(*loc).clear()

    # 获取标题
    def get_title(self):
        return self.driver.title

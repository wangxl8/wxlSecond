from selenium.webdriver.common.by import By
from testcases.pom.pages.basePage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class CategoryPage(BasePage):
    # 文章loc
    click_article_loc = (By.XPATH, '//*[@id="article"]/a')
    # 分类loc
    click_category_loc = (By.XPATH, '//*[@id="分类--/admin/article/category"]/a')
    # 分类名称loc
    category_name_loc = (By.NAME, 'category.title')
    # 父分类loc
    parent_category_loc = (By.NAME, 'category.pid')
    # 固定链接loc
    slug_loc = (By.NAME, 'category.slug')
    # 提交按钮
    add_btn_loc = (By.CLASS_NAME, 'btn')

    def __init__(self, login):
        BasePage.__init__(self, login.driver)

    # 点击左侧栏的文章
    @allure.step('步骤：点击左侧栏文章菜单')
    def click_article(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_article_loc))
        self.click(*self.click_article_loc)
        self.logger.info('分类创建：点击左侧栏的文章')

    # 点击分类
    @allure.step('步骤：点击左侧栏文章下的分类菜单')
    def click_category(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_category_loc))
        self.click(*self.click_category_loc)
        self.logger.info('分类创建：点击左侧栏的分类')

    # 输入分类名称
    @allure.step('步骤：输入分类名称')
    def input_category_name(self, name):
        self.clear(*self.category_name_loc)
        self.type_text(name, *self.category_name_loc)
        self.logger.info('分类创建：输入分类名称：%s', name)

    # 选择父级分类
    @allure.step('步骤：选择父分类')
    def select_parent_category(self, parent_name):
        self.select(parent_name, *self.parent_category_loc)
        self.logger.info('分类创建：选择父分类：%s', parent_name)

    # 输入固定链接字段
    @allure.step('步骤：输入固定链接')
    def input_slug(self, slug):
        self.clear(*self.slug_loc)
        self.type_text(slug, *self.slug_loc)
        self.logger.info('分类创建：输入固定链接：%s', slug)

    # 点击添加
    @allure.step('步骤：点击添加按钮')
    def click_add_btn(self):
        self.click(*self.add_btn_loc)
        self.logger.info('分类创建：点击添加按钮')

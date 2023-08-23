from selenium.webdriver import ActionChains
from testcases.pom.pages.basePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import allure


@allure.feature('模块描述：文章管理')
class ArticlePage(BasePage):
    # 文章loc
    click_article_loc = (By.XPATH, '//*[@id="article"]/a')
    # 文章管理loc
    click_article_manage_loc = (By.XPATH, '//*[@id="文章管理--/admin/article/list"]/a')
    # 新建文章按钮loc
    click_add_article_btn_loc = (By.XPATH, '/html/body/div/div[1]/section[1]/div/div/div[2]/div/a')

    # 文章标题
    article_title_loc = (By.ID, 'article-title')
    # 文章内容
    body_loc = (By.XPATH, '//*[@id="form"]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/p')

    # 发布按钮
    add_btn_loc = (By.XPATH, '//*[@id="form"]/div/div[2]/div[1]/div/button[1]')

    # 文章链接
    article_link_loc = (By.XPATH, '/html/body/div/div[1]/section[2]/div/div/div[2]/table/tbody/tr/td[2]/strong/a')
    # 删除文章链接
    del_article_link_loc = (By.XPATH, '/html/body/div/div[1]/section[2]/div/div/div[2]/table/tbody/tr/td[2]/div/div/a[3]')

    # 文章全选按钮
    select_all_checkbox_loc = (By.ID, 'checkall')
    # 批量操作选项：删除
    del_all_select_loc = (By.NAME, 'action')
    # 批量操作（删除）按钮
    del_all_btn_loc = (By.XPATH, '/html/body/div/div[1]/section[2]/div/div/div[2]/div/div/div[1]/div/div[3]/button')

    @allure.step('步骤：管理员登录')
    def __init__(self, login):
        BasePage.__init__(self, login.driver)

    # 点击左侧栏的文章
    @allure.step('步骤：点击左侧栏文章菜单')
    def click_article(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.click_article_loc))
        self.click(*self.click_article_loc)
        self.logger.info('文章创建：点击左侧栏的文章')

    # 点击文章管理
    @allure.step('步骤：点击左侧栏文章管理菜单')
    def click_article_manage(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_article_manage_loc))
        self.click(*self.click_article_manage_loc)
        self.logger.info('文章创建：点击左侧栏的文章管理')

    # 点击添加文章
    @allure.step('步骤：点击添加文章按钮')
    def click_add_article(self):
        self.click(*self.click_add_article_btn_loc)
        self.logger.info('文章创建：点击添加文章按钮')

    # 输入文章标题
    @allure.step('步骤：输入文章标题')
    def input_article_title(self, title):
        self.type_text(title, *self.article_title_loc)
        self.logger.info('文章创建：输入文章标题：%s', title)

    # 输入文章内容
    @allure.step('步骤：输入文章内容')
    def input_body(self, body):
        self.type_text(body, *self.body_loc)
        self.logger.info('文章创建：输入文章内容：%s', body)

    # 点击添加按钮
    @allure.step('步骤：点击创建按钮')
    def click_add_btn(self):
        self.click(*self.add_btn_loc)
        self.logger.info('文章创建：点击创建按钮')

    # 删除单个文章
    def del_single_article(self):
        link = self.find_element(*self.article_link_loc)
        # 鼠标移动至文章链接上
        ActionChains(self.driver).move_to_element(link).perform()
        self.logger.info('单个文章删除：鼠标移至要删除的文章标题上，使其展示出删除按钮')

        self.click(*self.del_article_link_loc)
        self.logger.info('单个文章删除：点击移至垃圾箱，进行删除')

    # 删除所有文章
    def del_all_article(self):
        # 等待全选按钮可点击，并点击全选按钮
        self.click(*self.select_all_checkbox_loc)
        self.logger.info('批量删除：点击全选按钮')
        # 选择批量删除
        operate = self.driver.find_element(*self.del_all_select_loc)
        Select(operate).select_by_visible_text('批量删除')
        self.logger.info('批量删除：选择批量操作中的批量删除')
        # 点击删除按钮
        self.click(*self.del_all_btn_loc)
        self.logger.info('批量删除：点击确定按钮')
        # 等待二次确认弹窗出现，并点击确定
        btn = self.driver.find_element(By.CLASS_NAME, 'swal2-confirm')
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((btn)))
        btn.click()
        self.logger.info('批量删除：在二次确认弹窗中点击确定')
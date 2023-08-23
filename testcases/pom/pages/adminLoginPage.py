
from testcases.pom.pages.basePage import BasePage
from selenium.webdriver.common.by import By
import allure


class AdminLoginPage(BasePage):
    username_input = (By.NAME, 'user')
    pwd_input = (By.NAME, 'pwd')
    captcha_input = (By.ID, 'captcha')
    login_btn = (By.CLASS_NAME, 'btn')

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    @allure.step('步骤：进入管理员登录页面')
    def goto_admin_login_page(self):
        self.driver.get('http://localhost:8080/jpress/admin/login')
        self.driver.maximize_window()
        self.logger.info('管理员登录')

    @allure.step('步骤：输入用户名')
    def input_username(self, username):
        self.clear(*self.username_input)
        self.type_text(username, *self.username_input)
        self.logger.info('管理员登录：输入用户名：%s', username)

    @allure.step('步骤：输入密码')
    def input_pwd(self, pwd):
        self.clear(*self.pwd_input)
        self.type_text(pwd, *self.pwd_input)
        self.logger.info('管理员登录：输入密码：%s', pwd)

    @allure.step('步骤：输入验证码')
    def input_captcha(self, captcha):
        self.clear(*self.captcha_input)
        self.type_text(captcha, *self.captcha_input)
        self.logger.info('管理员登录：输入验证码：%s', captcha)

    @allure.step('步骤：点击登录按钮')
    def click_login_btn(self):
        self.click(*self.login_btn)
        self.logger.info('管理员登录：点击登录按钮')

from selenium.webdriver.common.by import By

from testcases.pom.pages.basePage import BasePage
import allure


class UserRegisterPage(BasePage):

    username_input = (By.NAME, 'username')
    email_input = (By.NAME, 'email')
    pwd_input = (By.NAME, 'pwd')
    confirmPwd_input = (By.NAME, 'confirmPwd')
    captcha_input = (By.ID, 'captcha')
    register_btn = (By.CLASS_NAME, 'btn')

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    @allure.step('步骤：进入用户注册页面')
    def goto_register_page(self):
        self.driver.get('http://localhost:8080/jpress/user/register')
        self.driver.maximize_window()
        self.logger.info('用户注册')

    @allure.step('步骤：输入注册用户名')
    def input_username(self, username):
        self.clear(*self.username_input)
        self.type_text(username, *self.username_input)
        self.logger.debug('用户注册：输入用户名：%s', username)

    @allure.step('步骤：输入邮箱')
    def input_email(self, email):
        self.clear(*self.pwd_input)
        self.type_text(email, *self.email_input)
        self.logger.debug('用户注册：输入邮箱：%s', email)

    @allure.step('步骤：输入密码')
    def input_pwd(self, pwd):
        self.clear(*self.pwd_input)
        self.type_text(pwd, *self.pwd_input)
        self.logger.debug('用户注册：输入密码：%s', pwd)

    @allure.step('步骤：输入确认密码')
    def input_confirmPwd(self, confirmPwd):
        self.clear(*self.confirmPwd_input)
        self.type_text(confirmPwd, *self.confirmPwd_input)
        self.logger.debug('用户注册：输入确认密码：%s', confirmPwd)

    @allure.step('步骤：输入验证码')
    def input_captcha(self, captcha):
        self.clear(*self.captcha_input)
        self.type_text(captcha, *self.captcha_input)
        self.logger.debug('用户注册：输入验证码：%s', captcha)

    @allure.step('步骤：点击注册按钮')
    def click_register_btn(self):
        self.click(*self.register_btn)
        self.logger.debug('用户注册：点击注册按钮')
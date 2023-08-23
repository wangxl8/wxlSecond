import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from testcases.pom.pages.userLoginPage import UserLoginPage

from util import util
import allure
import os


@allure.feature('模块描述：用户登录页面')
class TestUserLogin(object):
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\data\\data.xlsx"
    login_data = util.get_excel_rowdata(file_path, 'login')

    # login_data = [
    #     ('wxl',  '123456', '', '验证码不能为空'),
    #     ('wxl', '123456', '111', '用户中心')
    # ]

    def setup_class(self) -> None:
        self.driver = webdriver.Chrome()
        self.loginPage = UserLoginPage(self.driver)
        self.loginPage.goto_login_page()

    @allure.story('故事点：用户登录测试')
    @pytest.mark.parametrize('username, pwd, captcha, excepted', login_data)
    def test_user_login(self, username, pwd, captcha, excepted):
        # 输入用户名和密码
        self.loginPage.input_username(username)
        self.loginPage.input_pwd(pwd)
        # 判断是否自动识别验证码
        if captcha != '':
            captcha = util.get_code(self.driver, 'captcha-img')
        self.loginPage.input_captcha(captcha)

        self.loginPage.click_login_btn()

        # 使用断言验证
        if captcha != '':
            WebDriverWait(self.driver, 5).until(EC.title_is(excepted))
            # 如果不符合预期，输出失败日志
            try:
                assert self.driver.title == excepted
            except AssertionError:
                self.loginPage.logger.error("小王，程序%s", "断言失败，登录流程报错啦", exc_info=1)
            assert self.driver.title == excepted

        else:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            # 如果不符合预期，输出失败日志
            try:
                assert alert.text == excepted
            except AssertionError:
                self.loginPage.logger.error("小王，程序%s", "断言失败，登录流程报错啦", exc_info=1)
            assert alert.text == excepted
            alert.accept()


if __name__ == '__main__':
    pytest.main(['test_UserLogin.py'])

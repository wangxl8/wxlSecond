import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from testcases.pom.pages.adminLoginPage import AdminLoginPage

from util import util
import allure
import os


@allure.feature('模块描述：管理员登录页面')
class TestAdminLogin(object):
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\data\\data.xlsx"

    admin_login_data = util.get_excel_rowdata(file_path, 'adminlogin')

    # admin_login_data = [
    #     # ('wxl',  '123456', '111', '验证码不正确，请重新输入'),
    #     ('wxl', '123456', '222', 'JPress后台')
    # ]

    def setup_class(self) -> None:
        self.driver = webdriver.Chrome()
        self.adminLoginPage = AdminLoginPage(self.driver)
        self.adminLoginPage.goto_admin_login_page()

    # 测试管理员登录错误步骤省去
    @allure.story('故事点：管理员登录测试')
    @pytest.mark.dependency(name='admin_login')
    @pytest.mark.parametrize('username, pwd, captcha, excepted', admin_login_data)
    def test_admin_login(self, username, pwd, captcha, excepted):
        # 输入用户名和密码
        self.adminLoginPage.input_username(username)
        self.adminLoginPage.input_pwd(pwd)
        # 判断是否自动识别验证码
        if captcha != '111':
            captcha = util.get_code(self.driver, 'captcha-img')

        self.adminLoginPage.input_captcha(captcha)

        self.adminLoginPage.click_login_btn()

        # 使用断言验证
        if captcha != '111':
            WebDriverWait(self.driver, 5).until(EC.title_is(excepted))
            try:
                assert self.driver.title == excepted
            except AssertionError:
                self.adminLoginPage.logger.error("小王，程序%s", "断言失败，管理员登录流程报错啦", exc_info=1)
            assert self.driver.title == excepted

        else:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            try:
                assert alert.text == excepted
            except AssertionError:
                self.adminLoginPage.logger.error("小王，程序%s", "断言失败，管理员登录流程报错啦", exc_info=1)
            assert alert.text == excepted
            alert.accept()


if __name__ == '__main__':
    pytest.main(['test_AdminLogin.py'])
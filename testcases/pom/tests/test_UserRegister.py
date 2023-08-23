import pytest
from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from testcases.pom.pages.userRegisterPage import UserRegisterPage

from util import util
import allure


@allure.feature('模块描述：用户注册页面')
class TestUserRegister(object):

    login_data = util.get_excel_rowdata(r'C:\pythonProject\wxlSecond\data\data.xlsx', 'register')
    # login_data = [
    #     ('test01', 'test001@qq.com', '123456', '123456', '666', '验证码不正确'),
    #     ('XX', 'XX@qq.com', '123456', '123456', '111', '注册成功，点击确定进行登录。')
    # ]

    def setup_class(self) -> None:
        self.driver = webdriver.Chrome()
        self.registerPage = UserRegisterPage(self.driver)
        self.registerPage.goto_register_page()

    @allure.story('故事点：用户注册测试')
    @pytest.mark.parametrize('username,email,pwd,confirmPwd,captcha,expected', login_data)
    def test_register(self, username, email, pwd, confirmPwd, captcha, expected):
        # 若要和失败一起测，则需要先清空输入框中的内容
        # 找到元素进行输入
        # 使用随机的用户名和邮箱组合
        if username != 'test01':
            username = util.get_random_str()
            email = username + '@qq.com'
        self.registerPage.input_username(username)
        self.registerPage.input_email(email)
        self.registerPage.input_pwd(pwd)
        self.registerPage.input_confirmPwd(confirmPwd)

        # 自动识别验证码
        if captcha != '666':
            captcha = util.get_code(self.driver, 'captcha-img')

        # 输入验证码
        self.registerPage.input_captcha(captcha)
        # 点击注册
        self.registerPage.click_register_btn()

        # 等待alert出现
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert

        #  python中的断言
        # 如果不符合预期，输出失败日志
        try:
            assert alert.text == expected
        except AssertionError:
            self.registerPage.logger.error("小王，程序%s", "断言失败，注册流程报错啦", exc_info=1)
        assert alert.text == expected
        alert.accept()


if __name__ == '__main__':
    pytest.main(['test_UserRegister.py'])

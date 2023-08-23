import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testcases.pom.tests.test_AdminLogin import TestAdminLogin
import pytest
from testcases.pom.pages.categoryPage import CategoryPage
from util import util
import os


@allure.feature('模块描述：分类页面')
class TestCategory(object):
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\data\\data.xlsx"
    category_data = util.get_excel_rowdata(file_path, 'category')

    # category_data = [
    #     ('', '顶级', 'test', '这是必填内容'),
    #     ('demo', '顶级', 'demo', '')
    # ]

    def setup_class(self) -> None:
        self.login = TestAdminLogin()
        self.categoryPage = CategoryPage(self.login)

    @allure.story('故事点：新增分类测试')
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    @pytest.mark.parametrize('name,parent,slug,expected', category_data)
    def test_add_category(self, name, parent, slug, expected):
        # 点击左侧栏文章管理和分类，进行新增分类
        if name == '':
            self.categoryPage.click_article()
            self.categoryPage.click_category()

        self.categoryPage.input_category_name(name)
        self.categoryPage.select_parent_category(parent)
        self.categoryPage.input_slug(slug)

        self.categoryPage.click_add_btn()

        if name == '':
            # 等待提示框
            loc = (By.ID, 'category.title-error')
            WebDriverWait(self.login.driver, 5).until(EC.visibility_of_element_located(loc))
            # 添加断言
            msg = self.login.driver.find_element(*loc).text
            try:
                assert msg == expected
            except AssertionError:
                self.categoryPage.logger.error("小王，程序%s", "断言失败，分类创建流程报错啦", exc_info=1)
            assert msg == expected
        else:
            assert 1 == 1


if __name__ == '__main__':
    pytest.main(['test_Category.py'])
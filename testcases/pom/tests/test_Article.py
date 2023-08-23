import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from testcases.pom.pages.articlePage import ArticlePage
from testcases.pom.tests.test_AdminLogin import TestAdminLogin
from util import util
import allure


@allure.feature('模块描述：文章管理页面')
class TestArticle(object):
    article_data = util.get_excel_rowdata(r'C:\pythonProject\wxlSecond\data\data.xlsx', 'article')
    # article_data = [
    #     ('我的文章01', '我的文章内容01', '×\n文章保存成功。'),
    #     ('我的文章02', '我的文章内容02', '×\n文章保存成功。'),
    #     ('我的文章03', '我的文章内容03', '×\n文章保存成功。')
    # ]

    def setup_class(self) -> None:
        self.login = TestAdminLogin()
        self.articlePage = ArticlePage(self.login)
        self.articlePage.click_article()

    # 测试添加文章
    @allure.story('故事点：新增文章测试')
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    @pytest.mark.parametrize('title, content, expected', article_data)
    def test_add_ok(self, title, content, expected):
        # 点击侧边栏菜单进入页面
        self.articlePage.click_article_manage()
        self.articlePage.click_add_article()

        # 输入文章内容
        self.articlePage.input_article_title(title)
        self.articlePage.input_body(content)
        self.articlePage.click_add_btn()

        # 获取保存成功提示，进行断言
        loc = (By.CLASS_NAME, 'toast-success')
        WebDriverWait(self.login.driver, 5).until(EC.visibility_of_element_located(loc))
        msg = self.login.driver.find_element(*loc).text
        try:
            assert msg == '×\n' + expected
        except AssertionError:
            self.articlePage.logger.error("小王，程序%s", "断言失败，新建文章流程报错啦", exc_info=1)
        assert msg == '×\n' + expected

    # 测试删除单个文章
    @allure.story('故事点：删除单个文章测试')
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_delete_one_article_ok(self):
        # 直接点击文章管理，进行删除文章
        self.articlePage.click_article_manage()
        self.articlePage.del_single_article()
        sleep(2)

    # 测试删除所有文章
    @allure.story('故事点：删除全部文章测试')
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_delete_all_article_ok(self):
        self.articlePage.del_all_article()


if __name__ == '__main__':
    pytest.main(['test_Article.py'])
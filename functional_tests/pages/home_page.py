from functional_tests.base import wait
from .base_page import BasePage

class HomePage(BasePage):

    def get_page_title(self):
        return self.test.browser.find_element_by_css_selector('.ms-site-title.ms-site-title-lg')


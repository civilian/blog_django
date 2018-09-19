from functional_tests.base import wait
from functional_tests.base_page import BasePage

class HomePage(BasePage):

    def go_to_home_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_link_text('Posts')
        )
        return self

    def get_page_title(self):
        return self.test.browser.find_element_by_css_selector('.ms-site-title.ms-site-title-lg')

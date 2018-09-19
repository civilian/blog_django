
from .base import FunctionalTest
from functional_tests.home_page import HomePage

class LayoutAndStyling(FunctionalTest):

    def test_layout_and_styling(self):
        #  Nato goes to the home page
        self.browser.get(self.live_server_url)

        home_page = HomePage(self).go_to_home_page()

        self.browser.set_window_size(1024, 768)

        # He notices the title of the page is nicely centered

        pagetitle = home_page.get_page_title()
        self.assertAlmostEqual(
            pagetitle.location['x'] + pagetitle.size['width'] / 2,
            512,
            delta=10
        )

from .index_base_page import IndexBasePage
from functional_tests.base import wait

class IndexPostPage(IndexBasePage):

    def go_to_index_post_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_link_text('Posts').click()
        )
        self.test.browser.find_element_by_link_text('Show All Posts').click()
        self.test.wait_for(lambda: self.test.assertIn(
            'All Posts',
            [ title.text for title in self.test.browser.find_elements_by_tag_name('h1')]
        ))
        return self

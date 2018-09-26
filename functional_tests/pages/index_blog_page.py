from .index_base_page import IndexBasePage
from functional_tests.base import wait

class IndexBlogPage(IndexBasePage):

    def go_to_index_blog_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(lambda: self.test.assertIn(
            'Blog Django',
            [ title.text for title in self.test.browser.find_elements_by_tag_name('h1')]
        ))
        return self

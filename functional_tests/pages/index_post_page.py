from .base_page import BasePage
from functional_tests.base import wait

class IndexPostPage(BasePage):

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


    def get_posts_for_this_page(self):
        self.test.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self.test.browser.find_elements_by_tag_name('article')

    @wait
    def wait_for_title_post_in_the_posts(self, title_text):
        posts = self.get_posts_for_this_page()
        for post in posts:
            if title_text in post.text:
                return True
        raise AssertionError(f'{title_text} not found inside {[post.text for post in posts]}')


    def get_post_from_this_page(self, title_text):
        posts = self.get_posts_for_this_page()
        for post in posts:
            if title_text in post.text:
                return post

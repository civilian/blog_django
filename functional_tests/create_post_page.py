from functional_tests.base import wait

class CreatePostPage(object):

    def __init__(self, test):
        self.test = test


    def go_to_create_post_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_link_text('Posts').click()
        )
        self.test.browser.find_element_by_link_text('Create New Post').click()
        self.test.wait_for(lambda: self.test.assertIn(
            'Create New Post',
            [ e.text for e in self.test.browser.find_elements_by_tag_name('h1')]
        ))
        return self


    def write_in_title_input_box(self, text):
        title = self.find_element_by_id('id_title')
        title.send_keys(text)


    def write_in_content_input_box(self, text):
        title = self.find_element_by_id('id_content')
        title.send_keys(text)

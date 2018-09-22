from functional_tests.base import wait
from .post_form_page import PostFormPage

class CreatePostPage(PostFormPage):

    def go_to_create_post_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_link_text('Posts').click()
        )
        self.test.browser.find_element_by_link_text('Create New Post').click()
        self.test.wait_for(lambda: self.test.assertIn(
            'Create New Post',
            [ title.text for title in self.test.browser.find_elements_by_tag_name('h1')]
        ))
        return self


    def click_create_post(self):
        self.test.browser.find_element_by_name('create post').click()


    def create_post(self, post):
        self.go_to_create_post_page()
        self.write_in_title_input_box(post.title)
        self.write_in_content_input_box(post.content)
        # He puts the image for the post
        ## TODO:
        self.write_expiring_date(post.expiring_date.strftime('%Y-%m-%d'))
        self.click_create_post()
        self.check_message_in_messages('The blog post has been created')
        return self

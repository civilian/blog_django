import time

from .base import FunctionalTest
from functional_tests.create_post_page import CreatePostPage

class RegisterAPostTest(FunctionalTest):

    def test_can_register_a_post(self):
        # Nato goes to check the home page of the new blog app
        # he has heard about
        self.browser.get(self.live_server_url)

        # He notices the page title and the header mentions posts
        self.assertIn('Blog', self.browser.title)

        # He sees an invitation to create a new post and he clicks it
        create_post_page = CreatePostPage(self).go_to_create_post_page()

        # He is taken to a new page were he encounters different fields
        # he needs to fill.

        # He starts to filling the title of the post
        create_post_page.write_in_title_input_box('Awesome blog post')

        # Then he fills the content of the post
        create_post_page.write_in_content_input_box('Content of the post')

        ## TODO: PUT THE REST OF THE FIELDS

        # He after finish saves the blog post
        self.find_element_by_link_text('Create post').click()

        # The page shows him a success message telling him the blog has been
        # created
        navbar = self.find_element_by_css_selector('.navbar')
        self.assertIn('The blog post has been created', navbar)

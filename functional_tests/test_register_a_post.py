import datetime

from .base import FunctionalTest
from functional_tests.create_post_page import CreatePostPage
from posts.tests import util

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

        # He starts to fill the title of the post
        create_post_page.write_in_title_input_box('Awesome blog post')

        # Then he fills the content of the post
        create_post_page.write_in_content_input_box('Content of the post')

        # He puts the image for the post
        ## TODO:

        # And he puts the expiration date
        expiring_date = util.get_date_with_time_delay(7)
        create_post_page.write_expiring_date(expiring_date)


        # He after finish saves the blog post
        create_post_page.click_create_post()

        # The page shows him a success message telling him the blog has been
        # created
        create_post_page.check_message_in_messages('The blog post has been created')

        # And the page shows the content of the post
        body_text = self.browser.find_element_by_tag_name('body').text

        self.assertIn('Awesome blog post', body_text)
        self.assertIn('Content of the post', body_text)
        self.assertIn(expiring_date, body_text)

        # Satisfied Nato goes back to sleep

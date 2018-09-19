import datetime

from .base import FunctionalTest
from functional_tests.create_post_page import CreatePostPage
from posts.tests import util
from posts.forms import EXPIRATION_DATE_IS_WRONG

class RegisterAPostTest(FunctionalTest):

    def test_cannot_add_post_with_bad_expiration_date(self):
        # Nato goes blog and starts a new post
        self.browser.get(self.live_server_url)
        create_post_page = CreatePostPage(self).go_to_create_post_page()
        create_post_page.write_in_title_input_box('Awesome blog post')
        create_post_page.write_in_content_input_box('Content of the post')

        # He creates an expiring_date that does not make sense
        expiring_date = util.get_date_with_time_delay(-1)
        create_post_page.write_expiring_date(expiring_date)

        create_post_page.click_create_post()

        self.wait_for(lambda: self.assertEqual(
            create_post_page.get_error_element().text,
            EXPIRATION_DATE_IS_WRONG
        ))

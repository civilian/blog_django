import datetime

from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_post_page import IndexPostPage
from functional_tests.pages.edit_post_page import EditPostPage
from posts.tests import util
from posts.tests.util import PostFactory

class EditAPostTest(FunctionalTest):

    def test_can_edit_a_post(self):
        # Nato is a logged-in user
        self.create_pre_authenticated_session('nato')

        # He goes to the blog and creates a post
        post_object = PostFactory.build()
        CreatePostPage(self).create_post(post_object)

        # Then he proceeds to edit it
        # He first goes to the page of the post
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        post_html = index_post_page.get_post_from_this_page(post_object.title)
        post_html.find_element_by_link_text('EDIT POST').click()

        # Then he starts to edit the post field by field
        edit_post_page = EditPostPage(self)
        edit_post_page.write_in_title_input_box('New title')
        edit_post_page.write_in_content_input_box('New content')
        # He puts the image for the post
        ## TODO:
        today_plus_three_days = datetime.date.today() + datetime.timedelta(3)
        edit_post_page.write_expiring_date(today_plus_three_days.strftime('%Y-%m-%d'))

        # Then he presses the save button
        edit_post_page.click_save_post()
        edit_post_page.check_message_in_messages('The blog post has been updated')

        # And he can see the post has changed
        body_text = self.browser.find_element_by_tag_name('body').text

        self.assertIn('New title', body_text)
        self.assertIn('New content', body_text)
        self.assertIn(post_object.publication_date.strftime('%b. %d, %Y'), body_text)
        self.assertIn(today_plus_three_days.strftime('%b. %d, %Y'), body_text)

        # Satisfied Nato goes back to sleep

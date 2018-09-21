import datetime

from .base import FunctionalTest
from functional_tests.create_post_page import CreatePostPage
from posts.tests import util
from posts.tests.util import PostFactory

class RegisterAPostTest(FunctionalTest):

    def test_can_register_a_post(self):
        # Nato goes to check the home page of the new blog app
        # he has heard about
        self.browser.get(self.live_server_url)

        # He notices the page title and the header mentions posts
        self.assertIn('Blog', self.browser.title)

        # He sees an invitation to create a new post and he clicks it
        # He is taken to a new page were he encounters different fields
        # he needs to fill.
        # He fills them
        # He after finish saves the blog post
        # The page shows him a success message telling him the blog has been
        # created
        post = PostFactory()
        create_post_page = CreatePostPage(self).create_post(post)

        # He puts the image for the post
        ## TODO:


        # And the page shows the content of the post
        body_text = self.browser.find_element_by_tag_name('body').text

        self.assertIn(post.title, body_text)
        self.assertIn(post.content, body_text)
        self.assertIn(post.publication_date.strftime('%b. %d, %Y'), body_text)
        self.assertIn(post.expiring_date.strftime('%b. %d, %Y'), body_text)


        # Satisfied Nato goes back to sleep

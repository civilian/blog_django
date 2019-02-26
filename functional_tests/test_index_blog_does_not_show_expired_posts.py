import datetime
import time

from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_blog_page import IndexBlogPage
from posts.tests.util import PostFactory

class IndexBlogDoesNotShowExpiredPostTests(FunctionalTest):

    def test_index_blog_does_not_show_expired_post(self):
        # Nato is a logged-in user
        self.create_pre_authenticated_session('nato')

        # Nato goes to the blog and creates an expired post
        expired_post = PostFactory.build(title='Expired post')
        expired_post.publication_date = datetime.date.today() - datetime.timedelta(1)
        expired_post.expiring_date = expired_post.publication_date
        create_post_page = CreatePostPage(self).create_post(expired_post)

        # And creates a non expired post
        not_expired_post = PostFactory.build(title='Not expired post')
        not_expired_post.publication_date = datetime.date.today()
        not_expired_post.expiring_date = datetime.date.today()
        create_post_page.create_post(not_expired_post)
        
        # He can see the post in the index page of the posts
        index_post_page = IndexBlogPage(self).go_to_index_blog_page()
        index_post_page.wait_for_title_post_in_the_posts(not_expired_post.title)

        # And as expected he can't see the expired post
        body = self.browser.find_element_by_tag_name('body')       
        self.assertNotIn(expired_post.title, body.text)


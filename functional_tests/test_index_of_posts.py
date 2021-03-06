from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_post_page import IndexPostPage
from posts.tests.util import PostFactory

class IndexPostTests(FunctionalTest):

    def test_index_post_shows_and_can_be_consulted(self):
        # Nato goes to the blog and creates a posts and keeps the url
        first_post = PostFactory.build(title='First post title')
        create_post_page = CreatePostPage(self).create_post(first_post)
        first_post_url = self.browser.current_url

        # He can see the post in the index page of the posts
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        index_post_page.wait_for_title_post_in_the_posts(first_post.title)

        # He clicks the Read More link and can see that he is in the page
        # for that post
        post = index_post_page.get_post_from_this_page(first_post.title)
        post.find_element_by_link_text('READ MORE').click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_post_url)
        )

        # He creates another post and again saves the url
        second_post = PostFactory.build(title='Second post title')
        create_post_page.create_post(second_post)
        second_post_url = self.browser.current_url

        # And now he sees the new created post in the index
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        index_post_page.wait_for_title_post_in_the_posts(second_post.title)

        # And he checks is the page that shows him the post
        post = index_post_page.get_post_from_this_page(second_post.title)
        post.find_element_by_link_text('READ MORE').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_post_url)
        )

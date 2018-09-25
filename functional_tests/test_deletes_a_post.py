from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_post_page import IndexPostPage
from posts.tests.util import PostFactory

class DeletesAPostTests(FunctionalTest):

    def test_can_delete_a_post(self):
        # Nato goes to the blog and creates two post
        first_post = PostFactory.build(title='First post title')
        second_post = PostFactory.build(title='Second post title')
        CreatePostPage(self).create_post(first_post)
        CreatePostPage(self).create_post(second_post)

        # He can see the post in the index page of the posts
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        index_post_page.wait_for_title_post_in_the_posts(first_post.title)
        index_post_page.wait_for_title_post_in_the_posts(second_post.title)

        # He clicks the Delete button
        post = index_post_page.get_post_from_this_page(second_post.title)
        post.find_element_by_name('delete post').click()
        index_post_page.check_message_in_messages('The blog post has been succesfully deleted')

        # and he can see the post has been deleted
        body = self.browser.find_element_by_tag_name('body')        
        self.assertNotIn(second_post.title, body.text)
        index_post_page.wait_for_title_post_in_the_posts(first_post.title)


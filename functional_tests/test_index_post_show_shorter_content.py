from faker import Faker

from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_post_page import IndexPostPage
from posts.tests.util import PostFactory

class IndexPostShowsContentTruncatedTests(FunctionalTest):

    def test_index_post_shows_truncated_content(self):
        # Nato is a logged-in user
        self.create_pre_authenticated_session('nato')

        # Nato goes to the blog and creates a post with a long content
        post = PostFactory.build(title='First post title')
        fake = Faker()
        post.content=fake.sentence(nb_words=100)
        CreatePostPage(self).create_post(post)

        # He can see the post in the index page of the posts
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        post_html = index_post_page.get_post_from_this_page(post.title)

        # And he can see the content has been trimmed
        trimmed_content = post.content[:97] + '...'
        trimmed_content = trimmed_content.replace('\n', ' ')
        self.assertIn(trimmed_content, post_html.text)
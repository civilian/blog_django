import datetime

from selenium import webdriver

from .base import FunctionalTest
from functional_tests.pages.create_post_page import CreatePostPage
from functional_tests.pages.index_blog_page import IndexBlogPage
from functional_tests.pages.index_post_page import IndexPostPage
from functional_tests.pages.edit_post_page import EditPostPage
from posts.tests import util
from posts.tests.util import PostFactory

def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class PublicationDateAjax(FunctionalTest):

    def test_publication_date_updates_asynchronous(self):
        # Nato goes to the blog and creates a post
        post_object = PostFactory.build()
        CreatePostPage(self).create_post(post_object)
        first_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(first_browser))

        # And he can see it
        index_blog_page = IndexBlogPage(self).go_to_index_blog_page()
        index_blog_page.wait_for_title_post_in_the_posts(post_object.title)

        # Then he proceeds to edit it in another browser
        second_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(second_browser))
        self.browser = second_browser

        # He first goes to the page of the post
        index_post_page = IndexPostPage(self).go_to_index_post_page()
        post_html = index_post_page.get_post_from_this_page(post_object.title)
        post_html.find_element_by_link_text('EDIT POST').click()

        # Then he starts to edit the post publication date
        edit_post_page = EditPostPage(self)
        today_plus_three_days = datetime.date.today() + datetime.timedelta(3)
        edit_post_page.write_publication_date(today_plus_three_days.strftime('%Y-%m-%d'))
        ## Change the focus so the event is complete
        edit_post_page.write_in_title_input_box("")

        # And he sees a message telling him the publication date has changed whitout saving 
        # the post
        edit_post_page.check_message_in_messages("The publication date has been saved.")


        # And he can see the post has dissapeared from the index blog page
        self.browser = first_browser
        index_blog_page = IndexBlogPage(self).go_to_index_blog_page()
        body_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn(post_object.title, body_text)
        # Satisfied Nato goes back to sleep

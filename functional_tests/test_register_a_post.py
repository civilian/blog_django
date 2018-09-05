from .base import FunctionalTest

class RegisterAPostTest(FunctionalTest):

    def test_can_register_a_post(self):
        # Nato goes to check the home page of the new blog app
        # he has heard about
        self.browser.get(self.live_server_url)

        # He notices the page title and the header mentions posts
        self.assertIn('Blog', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('Blog', header_text)

        # He sees an invitation to create a new post and he clicks it
        self.browser.find_element_by_link_text('Create New Post').click()

        # He is taken to a new page were he encounters different fields
        # he needs to fill.
        self.waith_for(
            self.browser.find_element_by_name('Create new post')
        )

        # He starts to fill the fields of the post
        title = self.find_element_by_id('id_title')
        title.send_keys('Awesome blog post')

        ## TODO: PUT THE REST OF THE FIELDS

        # He after finish saves the blog post
        self.find_element_by_link_text('Create post').click()

        # The page shows him a success message telling him the blog has been
        # created
        navbar = self.find_element_by_css_selector('.navbar')
        self.assertIn('The blog post has been created', navbar)

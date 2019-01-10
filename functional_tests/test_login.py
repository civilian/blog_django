from .base import FunctionalTest
from functional_tests.pages.home_page import HomePage

class LoginTest(FunctionalTest):

    def test_can_create_user_and_log_in(self):
        # Nato goes to the new blog app 
        # and notices a person icon he clicks it
        home_page = HomePage(self).go_to_home_page()
        self.fail('Finish the test!!')
        home_page.click_account_button()

        # Now he can see a couple of tabs so he clicks the tab
        # That says register
        


        # He fills the username, the email, the password, and
        # Retypes the password

        # He clicks the register now button

        # The page tells him his user has been created

        # Now he proceds to log in
        # He first goes to the index page and clicks the person
        # icon again

        # Now he goes to the login tab

        # And he introduces his username and his password

        # And he clicks the login button

        # Now the page tells him he is logged in
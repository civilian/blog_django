from .base import FunctionalTest
from functional_tests.pages.account_register_popup_window import AccountRegisterPopupWindow
from accounts.tests.util import UserFactory

class LoginTest(FunctionalTest):

    def test_can_create_user_and_log_in(self):
        # Nato goes to the new blog app 
        # and notices a person icon he clicks it

        # Now he can see a couple of tabs so he clicks the tab
        # That says register

        # He fills the username, the email, the password, and
        # Retypes the password

        # He clicks the register now button

        # And the page tells him his user has been created
        user = UserFactory.build()
        account_register_popup = AccountRegisterPopupWindow(self).create_user(user)  

        # Now he proceds to log in
        # He first goes to the index page and clicks the person
        # icon again

        # Now he goes to the login tab

        # And he introduces his username and his password

        # And he clicks the login button

        # Now the page tells him he is logged in
from .base import FunctionalTest
from functional_tests.pages.account_register_popup_window import AccountRegisterPopupWindow
import time

class LoginTest(FunctionalTest):

    def test_can_create_user_and_log_in(self):
        # Nato goes to the new blog app 
        # and notices a person icon he clicks it

        # Now he can see a couple of tabs so he clicks the tab
        # That says register
        account_register_popup = AccountRegisterPopupWindow(self).go_to_register_popup()

        # He fills the username, the email, the password, and
        # Retypes the password
        account_register_popup.write_in_username_input_box('nato')
        account_register_popup.write_in_email_input_box('nato@nato.com')
        account_register_popup.write_in_password_input_box('natopassword')
        account_register_popup.write_in_retype_password_input_box('natopassword')

        # He clicks the register now button
        account_register_popup.click_register_button()

        # The page tells him his user has been created

        # Now he proceds to log in
        # He first goes to the index page and clicks the person
        # icon again

        # Now he goes to the login tab

        # And he introduces his username and his password

        # And he clicks the login button

        # Now the page tells him he is logged in
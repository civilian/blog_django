from .base import FunctionalTest
from functional_tests.pages.account_signup_popup_window import AccountSignupPopupWindow
from functional_tests.pages.account_login_popup_window import AccountLoginPopupWindow
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
        AccountSignupPopupWindow(self).create_user(user)  

        # Now he proceds to log in
        # He first goes to the index page and clicks the person
        # icon again

        # Now he goes to the login tab
        account_login_popup_window = AccountLoginPopupWindow(self).go_to_login_popup()

        # And he introduces his username and his password
        account_login_popup_window.write_in_username_input_box(user.username)
        account_login_popup_window.write_in_password_input_box(user.password)

        # And he clicks the login button
        account_login_popup_window.click_login_button()

        # Now the page tells him he is logged in
        account_login_popup_window.check_message_in_messages('The user has been logged in')
from .base import FunctionalTest
from functional_tests.pages.account_signup_popup_window import AccountSignupPopupWindow
from accounts.tests.util import UserFactory

class SignupFailsWithRepeatedUserTest(FunctionalTest):

    def test_signup_fails_with_repeated_user(self):
        # Nato goes to the new blog app 
        # and notices a person icon he clicks it

        # Now he can see a couple of tabs so he clicks the tab
        # That says register

        # He fills the username, the email, the password, and
        # Retypes the password

        # He clicks the register now button

        # And the page tells him his user has been created
        user = UserFactory.build()
        account_register_popup = AccountSignupPopupWindow(self).create_user(user)        

        # Todd goes to the new blog app
        # He clicks a person icon and clicks it
        # Now he can see a couple of tabs so he clicks the tab
        # That says register
        account_register_popup.go_to_signup_popup()

        # He fills the username but he likes to call himself nato
        # In every page
        account_register_popup.write_in_username_input_box(user.username)

        # He fills the email, the password and retype the password
        account_register_popup.write_in_email_input_box('other@email.com')
        account_register_popup.write_in_password_input_box('otherpassword')
        account_register_popup.write_in_retype_password_input_box('otherpassword')
        account_register_popup.click_signup_button()

        # As the username was repeated he gets an error message
        account_register_popup.check_message_in_messages('The password is wrong or the user has already been created')

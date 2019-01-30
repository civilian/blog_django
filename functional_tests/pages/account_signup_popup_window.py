from .account_base_popup_window import AccountBasePopupWindow
from functional_tests.base import wait

class AccountSignupPopupWindow(AccountBasePopupWindow):

    def go_to_signup_popup(self):
        self.go_to_account_popup()
        self.test.browser.find_element_by_id('id_signup_tab').click()
        return self
    

    def write_in_email_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_email')
    

    def write_in_retype_password_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_retype_password')
    
    
    def click_signup_button(self):
        self.test.browser.find_element_by_name('register now').click()
    

    def create_user(self, user):
        self.go_to_signup_popup()
        self.write_in_username_input_box(user.username)
        self.write_in_email_input_box(user.email)
        self.write_in_password_input_box(user.password)
        self.write_in_retype_password_input_box(user.password)
        self.click_signup_button()
        self.check_message_in_messages('The user has been created')
        return self
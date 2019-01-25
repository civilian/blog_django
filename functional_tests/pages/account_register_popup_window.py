from .account_base_popup_window import AccountBasePopupWindow
from functional_tests.base import wait

class AccountRegisterPopupWindow(AccountBasePopupWindow):

    def go_to_register_popup(self):
        self.go_to_account_popup()
        self.test.browser.find_element_by_id('id_register_tab').click()
        return self

    def write_in_username_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_username')
    

    def write_in_email_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_email')
    

    def write_in_password_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_password')
    

    def write_in_retype_password_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_retype_password')
    
    
    def click_register_button(self):
        self.test.browser.find_element_by_name('register now').click()
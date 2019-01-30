from .base_page import BasePage
from functional_tests.base import wait

class AccountBasePopupWindow(BasePage):

    def go_to_account_popup(self):
        self.go_to_home_page()
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_id('id_account_button').click()
        )
        return self
    
    
    def write_in_username_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_username')
    
    
    def write_in_password_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_password')

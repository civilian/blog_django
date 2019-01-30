from .account_base_popup_window import AccountBasePopupWindow
from functional_tests.base import wait

class AccountLoginPopupWindow(AccountBasePopupWindow):

    def go_to_login_popup(self):
        self.go_to_account_popup()
        self.test.browser.find_element_by_id('id_login').click()
        return self
    
    
    def click_login_button(self):
        self.test.browser.find_element_by_name('login').click()
 
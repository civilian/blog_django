from functional_tests.base import wait

class BasePage(object):

    def __init__(self, test):
        self.test = test

    @wait
    def check_message_in_messages(self, text_message):
        messages = self.test.browser.find_elements_by_css_selector('#messages div')
        self.test.assertIn(text_message, [message.text for message in messages])


    def get_error_element(self):
        return self.test.browser.find_element_by_css_selector('.errorlist')

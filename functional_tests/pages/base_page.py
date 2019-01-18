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
    

    def write_in_any_input(self, text, id):
        input = self.test.browser.find_element_by_id(id)
        input.clear()
        input.send_keys(text)
    

    def go_to_home_page(self):
        self.test.browser.get(self.test.live_server_url)
        self.test.wait_for(
            lambda: self.test.browser.find_element_by_link_text('Posts')
        )
        return self

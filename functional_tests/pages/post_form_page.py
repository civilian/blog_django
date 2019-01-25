from .base_page import BasePage

class PostFormPage(BasePage):

    def write_in_any_input(self, text, id):
        input = self.test.browser.find_element_by_id(id)
        input.clear()
        input.send_keys(text)

    def write_in_title_input_box(self, text):
        self.write_in_any_input(text, 'id_title')


    def write_in_content_input_box(self, text):
        self.write_in_any_input(text, 'id_content')


    def write_expiring_date(self, date_text):
        self.write_in_any_input(date_text, 'id_expiring_date')
    

    def write_publication_date(self, date_text):
        self.write_in_any_input(date_text, 'id_publication_date')

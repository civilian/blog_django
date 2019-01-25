from .base_page import BasePage

class PostFormPage(BasePage):

    def write_in_title_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_title')


    def write_in_content_input_box(self, text):
        self.write_in_any_input_by_id(text, 'id_content')


    def write_expiring_date(self, date_text):
        self.write_in_any_input_by_id(date_text, 'id_expiring_date')
    

    def write_publication_date(self, date_text):
        self.write_in_any_input_by_id(date_text, 'id_publication_date')

from .post_form_page import PostFormPage


class EditPostPage(PostFormPage):

    def click_save_post(self):
        self.test.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.test.browser.find_element_by_name('save changes').click()
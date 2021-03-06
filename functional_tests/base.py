import time
import os
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from .server_tools import reset_database
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

MAX_WAIT = 10

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        self.staging_ssh_user = os.environ.get('STAGING_SSH_USER')
        if self.staging_server:
            self.staging_port = os.environ.get('STAGING_PORT')
            if self.staging_port:
                self.live_server_url = f'http://{self.staging_server}:{self.staging_port}'
                self.staging_ssh_port = os.environ.get('STAGING_SSH_PORT')
                self.staging_ssh_private_key = os.environ.get('STAGING_SSH_PRIVATE_KEY')
                reset_database(self.staging_server, self.staging_ssh_user, self.staging_ssh_port, self.staging_ssh_private_key)
            else:
                self.live_server_url = 'http://' + self.staging_server
                reset_database(self.staging_server, self.staging_ssh_user)


    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()


    def _test_has_failed(self):
        return any(error for (method, error) in self._outcome.errors)


    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)


    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)


    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )


    @wait
    def wait_for(self, fn):
        return fn()


    def create_pre_authenticated_session(self, username):
        # TODO: Correct the staging server and the staging port
        if self.staging_server:
            if self.staging_port:
                session_key = create_session_on_server(
                                self.staging_server, username,
                                self.staging_ssh_user,
                                self.staging_ssh_port,
                                self.staging_ssh_private_key
                            )
            else:
                session_key = create_session_on_server(self.staging_server,
                                                        username, self.staging_ssh_user)
        else:
            # TODO: To create a user we will need more than an email
            session_key = create_pre_authenticated_session(username)
            print(session_key)

        ## to set a cookie we need to first  visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

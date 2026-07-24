from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage  # make sure the import path is correct
from pages.custom_exceptions  import TestExecutionException

class LoginPage(BasePage):


    USERNAME_INPUT = "input[data-test='username']"
    PASSWORD_INPUT = "input[data-test='password']"
    LOGIN_BUTTON = "input[data-test='login-button']"
    ERROR_SELECTOR = ".error-message-container"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------- Page Actions ----------
    def login(self, username, password):
        try:
            """Perform login action"""
            self.fill_text(self.USERNAME_INPUT, username)
            self.fill_text(self.PASSWORD_INPUT, password)
            self.click_element(self.LOGIN_BUTTON)
            # Optional: verify login success
            if self.is_error_displayed():
                raise TestExecutionException("Login failed with invalid credentials or locked-out user")
        except TestExecutionException as e:
            print("some error happened", e)

    def is_error_displayed(self, timeout=5) :
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_SELECTOR, timeout=timeout)

    def get_error_message(self, timeout= 5) :
        """Return error message text"""
        return self.get_text(self.ERROR_SELECTOR, timeout=timeout) if self.is_error_displayed(timeout) else ""


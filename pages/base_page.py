from abc import ABC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_page_load(self, timeout = 30):
        """Wait for page to be fully loaded"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_page_title(self) :
        """Get current page title"""
        return self.driver.title

    def get_current_url(self) :
        """Get current page URL"""
        return self.driver.current_url

    def click_element(self, selector , by: By = By.CSS_SELECTOR, timeout= 10):
        """Click element with wait"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        element.click()

    def fill_text(self, selector, text, by: By = By.CSS_SELECTOR, timeout= 10):
        """Fill text in input field"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, selector: str, by: By = By.CSS_SELECTOR, timeout= 10) -> str:
        """Get text from element"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        return element.text

    def is_element_visible(self, selector, by: By = By.CSS_SELECTOR, timeout= 5) -> bool:
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, selector))
            )
            return True
        except TimeoutException:
            return False

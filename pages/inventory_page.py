from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from typing import List
from pages.base_page import BasePage  # adjust import if needed


class InventoryPage(BasePage):
    # Locators
    INVENTORY_CONTAINER = ".inventory_container"
    HAMBURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    # ---------- Page Methods ----------
    def is_inventory_displayed(self) :
        return self.is_element_visible(self.INVENTORY_CONTAINER)

    def handle_alert_if_exists(self) :
        """Check if alert exists, accept it, and return True/False"""
        try:
            alert = self.driver.switch_to.alert
            print(f"Alert detected: {alert.text}")
            alert.accept()
            return True
        except NoAlertPresentException:
            return False


    def logout(self):
        """Logout from application"""
        self.handle_alert_if_exists()
        self.click_element(self.HAMBURGER_MENU)
        self.click_element(self.LOGOUT_LINK)

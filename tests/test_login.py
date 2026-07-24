import pytest
from selenium.webdriver.support.wait import WebDriverWait
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.test_data import TestData



class TestLogin:

    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.smoke
    def test_successful_login_standard_user(self, page, logger):
        """Test successful login with standard user"""
        logger.info(f"Testing successful login with standard user")
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.login(TestData.STANDARD_USER, TestData.PASSWORD)

        assert inventory_page.is_inventory_displayed()
        assert "inventory.html" in page.current_url


    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_locked_out_user(self, page, logger):
        """Test login with locked out user"""
        logger.info(f"Testing successful login with locked out user")
        login_page = LoginPage(page)

        login_page.login(TestData.LOCKED_OUT_USER, TestData.PASSWORD)

        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()


    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_invalid_credentials(self, page):
        """Test login with invalid credentials"""
        login_page = LoginPage(page)

        login_page.login(TestData.INVALID_USER, TestData.INVALID_PASSWORD)

        if login_page.is_error_displayed():
            logger.info("Error message displayed as expected")
        else:
            logger.error("Error message not displayed!")

        assert login_page.is_error_displayed()
        assert "username and passwords do not match" in login_page.get_error_message().lower()


    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_username(self, page):
        """Test login with empty username"""
        login_page = LoginPage(page)

        login_page.login("", TestData.PASSWORD)

        assert login_page.is_error_displayed()
        assert "username is required" in login_page.get_error_message().lower()


    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_with_empty_password(self, page):
        """Test login with empty password"""
        login_page = LoginPage(page)

        login_page.login(TestData.STANDARD_USER, "")

        assert login_page.is_error_displayed()
        assert "password is required" in login_page.get_error_message().lower()

#$timestamp = Get-Date -Format "yyyyMMdd_HHmmss
#pytest - m "ui" - -html = reports / report_$timestamp.html - -self - contained - html


    @pytest.mark.ui
    @pytest.mark.xfail(reason="Need to fix this")
    def test_logout_functionality(self, authenticated_page):
        """Test logout functionality"""
        inventory_page = InventoryPage(authenticated_page)
        login_page = LoginPage(authenticated_page)

        inventory_page.logout()

        # Wait until URL is back to login page
        WebDriverWait(authenticated_page, 20).until(
            lambda driver: driver.current_url == TestData.BASE_URL + "/"
        )

        # Should be back to login page
        assert authenticated_page.current_url  == TestData.BASE_URL + "/"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON)

    # def test_dummy_test(self, page):
    #     """Test dummy test"""
    #     assert 1 == 2

    def test_login_with_special_characters(self, page):
        """Test login with special characters in username and password"""
        login_page = LoginPage(page)

        special_username = "!@#$%^&*()_+"
        special_password = "!@#$%^&*()_+"

        login_page.login(special_username, special_password)

        assert login_page.is_error_displayed()
        assert "username and passwords do not match" in login_page.get_error_message().lower()
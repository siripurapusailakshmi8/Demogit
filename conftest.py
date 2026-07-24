import pytest
import requests
import logging
import os
from datetime import datetime
import requests_mock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.test_data import TestData
from utils.db_connection import DatabaseConnection


##################### Common fixtures for all test ##########################
@pytest.fixture(scope="session", autouse = True)
def logger():
    """Create a logger for all test cases."""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Configure logger
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logger = logging.getLogger("TestLogger")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers
        logger.addHandler(fh)
        logger.addHandler(ch)

    logger.info("Logger initialized")
    yield logger


@pytest.fixture(scope="module", autouse=True)
def module_logger(request, logger):
    """Log start and end of a test module automatically."""
    module_name = request.module.__name__
    logger.info(f"================ Starting tests in module: {module_name} ================")
    yield
    logger.info(f"================ Finished tests in module: {module_name} ================")

################################ UI related fixtures ###########################################


@pytest.fixture(scope="function")
def browser():
    """Create browser instance for the session with a clean temporary profile"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(20)  # Implicit wait
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def page(browser):
    browser.get(TestData.BASE_URL)
    yield browser
    browser.delete_all_cookies()


@pytest.fixture(scope="function")
def authenticated_page(page):
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.login(TestData.STANDARD_USER, TestData.PASSWORD)
    yield page



###################### API Related Fixtures ############################

BASE_URL = "https://dummy.restapiexample.com/api/v1"
@pytest.fixture(scope="session")
def mock_session():
    """Mocked session for API calls"""
    with requests_mock.Mocker() as m:
        session = requests.Session()

        # Mock POST /create
        m.post(f"{BASE_URL}/create", json={
            "status": "success",
            "data": {"id": 101, "employee_name": "Test Employee", "employee_salary": 50000, "employee_age": 30},
            "message": "Successfully! Record has been added."
        })

        # Mock GET /employee/101
        m.get(f"{BASE_URL}/employee/101", json={
            "status": "success",
            "data": {"id": 101, "employee_name": "Test Employee", "employee_salary": 50000, "employee_age": 30},
            "message": "Successfully! Record has been fetched."
        })

        # Mock PUT /update/101
        m.put(f"{BASE_URL}/update/101", json={
            "status": "success",
            "data": {"employee_salary": 60000},
            "message": "Successfully! Record has been updated."
        })

        # Mock DELETE /delete/101
        m.delete(f"{BASE_URL}/delete/101", json={
            "status": "success",
            "data": {"id": 101},
            "message": "Successfully! Record has been deleted."
        })

        yield session


@pytest.fixture
def employee(mock_session):
    """Setup: create a new employee; Teardown: delete after test"""
    # --- Setup ---
    payload = {
        "name": "Test Employee",
        "salary": "50000",
        "age": "30"
    }
    response = mock_session.post(f"{BASE_URL}/create", json=payload)
    assert response.status_code == 200
    emp_data = response.json()['data']
    employee_id = emp_data['id']

    yield employee_id  # Provide employee ID to the test

    # --- Teardown ---
    del_response = mock_session.delete(f"{BASE_URL}/delete/{employee_id}")
    assert del_response.status_code == 200


############### DB related fixtures #######################
@pytest.fixture(scope="session")
def db_connection():
    """Create DB connection for session"""
    db = DatabaseConnection(database="myapp")  # Replace with your DB name
    yield db
    db.close()


@pytest.fixture(scope="session")
def employees_table(db_connection):
    """Setup: create employees table; Teardown: drop table after test"""
    cursor = db_connection.get_cursor()

    # --- Setup: Create table ---
    create_table_query = """
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        salary INT NOT NULL,
        age INT NOT NULL
    )
    """
    cursor.execute(create_table_query)
    db_connection.commit()

    # Yield control to test
    yield cursor

    # Teardown: drop table
    cursor.execute("DROP TABLE IF EXISTS employees")
    db_connection.commit()


###################### Hooks ###########################
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # capture screenshot only on test failure
    if report.when == "call" and report.failed:
        if "browser" in item.fixturenames:
            driver = item.funcargs["browser"]
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, file_name)

            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved to: {screenshot_path}")




def pytest_configure(config):
    if not hasattr(config.option, "htmlpath") or not config.option.htmlpath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/report_{timestamp}.html"
        config.option.htmlpath = report_path
        config.option.self_contained_html = True

import pytest
import allure
from selenium import webdriver
from utils.data_loader import load_config
from utils.screen_recorder import ScreenRecorder
from utils.logger import test_logger

config = load_config()
driver = None

@pytest.fixture(params=["chrome"], scope="class")
def setup(request):
    """Fixture to initialize and quit the browser."""
    global driver
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()

    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def record_video():
    recorder = ScreenRecorder()
    recorder.start_recording()
    yield
    recorder.stop_recording()

@pytest.fixture(scope="function", autouse=True)
def log_test_start_and_end(request):
    test_logger.info(f"Starting test: {request.node.name}")
    yield
    test_logger.info(f"Test completed: {request.node.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)
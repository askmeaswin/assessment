import pytest
from selenium import webdriver
from utils.data_loader import load_config

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
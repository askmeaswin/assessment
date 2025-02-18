from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import test_logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        test_logger.info(f"check the url: {url}")
        self.driver.get(url)

    def click_element(self, locator):
        test_logger.info(f"Clicking element: {locator}")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()

    def get_elements_text(self, locator):
        test_logger.info(f"Clicking element: {locator}")
        return [elem.text for elem in self.driver.find_elements(*locator)]
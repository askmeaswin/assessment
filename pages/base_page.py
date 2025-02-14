from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def click_element(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()

    def get_elements_text(self, locator):
        return [elem.text for elem in self.driver.find_elements(*locator)]
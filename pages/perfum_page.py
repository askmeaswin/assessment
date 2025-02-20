from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import test_logger
import time


class ParfumPage(BasePage):
    PARFUM_BUTTON = (By.LINK_TEXT, "Parfum")
    COOKIE_BANNER = (By.ID, "usercentrics-root")
    ACCEPT_ALL_BUTTON_SELECTOR = "button[data-testid='uc-accept-all-button']"
    PRODUCT_SELECT = (By.XPATH, "//*[text()='{}']")
    PRODUCT_BY_VALUE = (By.XPATH, "//*[text()='{}']//ancestor::a[@role='checkbox']/span")
    POPUP_CLOSE = (By.XPATH, "//span[text()='Deine Meinung ist gefragt']//parent::div/button")
    PRODUCT_NAME_TEXT = (By.XPATH, "//button[text()='{}']")
    def accept_cookies(self):
        wait = WebDriverWait(self.driver, 15)
        try:
            shadow_host = wait.until(EC.presence_of_element_located(self.COOKIE_BANNER))
            test_logger.info("Cookie banner found.")
            wait.until(lambda driver: self.driver.execute_script("return arguments[0].shadowRoot", shadow_host) is not None)
            accept_button = wait.until(lambda driver: driver.execute_script(
                "return arguments[0].shadowRoot.querySelector(arguments[1])",
                shadow_host, self.ACCEPT_ALL_BUTTON_SELECTOR
            ))
            if accept_button is None:
                test_logger.error("Accept Cookies button not found inside Shadow DOM!")
                raise Exception("Accept Cookies button not found inside Shadow DOM!")
            wait.until(EC.element_to_be_clickable(accept_button))
            accept_button.click()
            test_logger.info("Accepted cookies.")
            self.click_element(self.PARFUM_BUTTON)
            test_logger.info("Clicked on 'Parfum' button.")
        except Exception as e:
            test_logger.error(f"Error in accept_cookies(): {e}")
            raise

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 15).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        test_logger.info("Page load complete.")

    def select_multiple_filters(self, filters_dict):
        wait = WebDriverWait(self.driver, 10)
        filter_items = list(filters_dict.items())
        for index, (filter_name, value) in enumerate(filter_items):
            if not value:
                continue
            try:
                self.wait_for_page_load()
                for _ in range(3):
                    try:
                        filter_locator = (By.XPATH, self.PRODUCT_SELECT[1].format(filter_name))
                        filter_element = wait.until(EC.element_to_be_clickable(filter_locator))
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_element)
                        filter_element.click()
                        test_logger.info(f"Selected filter: {filter_name}")
                        self.wait_for_page_load()
                        break
                    except StaleElementReferenceException:
                        test_logger.warning(f"Stale element for filter: {filter_name}. Retrying...")
                value_element = None
                for _ in range(3):
                    try:
                        value_locator = (By.XPATH, self.PRODUCT_BY_VALUE[1].format(value))
                        value_element = wait.until(EC.element_to_be_clickable(value_locator))
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", value_element)
                        value_element.click()
                        self.wait_for_page_load()
                        test_logger.info(f"Applied filter value: {value}")
                        break
                    except StaleElementReferenceException:
                        test_logger.warning(f"Stale element for value: {value}. Retrying...")
                if value_element is None:
                    raise TimeoutException(f"Failed to locate and click value '{value}' after retries.")
                applied_filter_locator = (By.XPATH, self.PRODUCT_NAME_TEXT[1].format(value))
                applied_filter_element = wait.until(EC.presence_of_element_located(applied_filter_locator))
                applied_filter_text = self.driver.execute_script("return arguments[0].textContent;", applied_filter_element)
                if applied_filter_text != value:
                    raise AssertionError(f"Expected filter '{value}', but found '{applied_filter_text}'.")
                test_logger.info(f"Verified applied filter: {applied_filter_text}")
                if index < len(filter_items) - 1:
                    wait.until(EC.staleness_of(value_element))
            except Exception as e:
                test_logger.error(f"Error selecting filter {filter_name}: {e}")
                raise
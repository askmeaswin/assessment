from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import test_logger


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
            self.click_element(self.POPUP_CLOSE)
            test_logger.info("Closed popup (if displayed).")
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

                filter_locator = (By.XPATH, self.PRODUCT_SELECT[1].format(filter_name))
                filter_element = wait.until(EC.element_to_be_clickable(filter_locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_element)
                filter_element.click()
                test_logger.info(f"Selected filter: {filter_name}")
                self.wait_for_page_load()
                value_locator = (By.XPATH, self.PRODUCT_BY_VALUE[1].format(value))
                value_element = wait.until(EC.element_to_be_clickable(value_locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", value_element)
                value_element.click()
                test_logger.info(f"Applied filter value: {value}")
                assert wait.until(EC.presence_of_element_located(self.PRODUCT_NAME_TEXT)), \
                    f"Filter {value} was not successfully applied."
                if index < len(filter_items) - 1:
                    wait.until(EC.staleness_of(value_element))
            except Exception as e:
                test_logger.error(f"Error selecting filter {filter_name}: {e}")
                raise
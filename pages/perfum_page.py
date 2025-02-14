from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ParfumPage(BasePage):
    PARFUM_BUTTON = (By.LINK_TEXT, "Parfum")
    COOKIE_BANNER = (By.ID, "usercentrics-root")
    ACCEPT_ALL_BUTTON_SELECTOR = "button[data-testid='uc-accept-all-button']"
    PRODUCT_SELECT = (By.XPATH, "//*[text()='{}']")
    PRODUCT_BY_VALUE = (By.XPATH, "//*[text()='{}']//ancestor::a[@role='checkbox']/span")
    POPUP_CLOSE = (By.XPATH, "//span[text()='Deine Meinung ist gefragt']//parent::div/button")
    def accept_cookies(self):
        """Waits for the page and shadow DOM to fully load, then accepts cookies."""
        wait = WebDriverWait(self.driver, 15)

        shadow_host = wait.until(EC.presence_of_element_located(self.COOKIE_BANNER))

        wait.until(lambda driver: self.driver.execute_script("return arguments[0].shadowRoot", shadow_host) is not None)

        # accept_button = find_element_in_shadow_root(self.driver, shadow_host, self.ACCEPT_ALL_BUTTON_SELECTOR)
        accept_button = wait.until(lambda driver: driver.execute_script(
            "return arguments[0].shadowRoot.querySelector(arguments[1])",
            shadow_host, self.ACCEPT_ALL_BUTTON_SELECTOR
        ))
        if accept_button is None:
            raise Exception("Accept Cookies button not found inside Shadow DOM!")
        wait.until(EC.element_to_be_clickable(accept_button))
        accept_button.click()
        self.click_element(self.PARFUM_BUTTON)
        self.click_element(self.POPUP_CLOSE)

    def wait_for_page_load(self):
        """Waits until the page is fully loaded (no ongoing AJAX requests)."""
        WebDriverWait(self.driver, 15).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def select_multiple_filters(self, filters_dict):
        """Selects multiple product filters dynamically with optimized waits."""
        wait = WebDriverWait(self.driver, 10)
        filter_items = list(filters_dict.items())
        for index, (filter_name, value) in enumerate(filter_items):
            if not value:
                continue
            self.wait_for_page_load()

            filter_locator = (By.XPATH, self.PRODUCT_SELECT[1].format(filter_name))
            filter_element = wait.until(EC.element_to_be_clickable(filter_locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_element)
            filter_element.click()
            self.wait_for_page_load()
            value_locator = (By.XPATH, self.PRODUCT_BY_VALUE[1].format(value))
            value_element = wait.until(EC.element_to_be_clickable(value_locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", value_element)
            value_element.click()
            if index < len(filter_items) - 1:
                wait.until(EC.staleness_of(value_element))
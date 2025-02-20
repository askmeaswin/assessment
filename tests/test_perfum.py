import pytest
from pages.perfum_page import ParfumPage
from utils.data_loader import load_config
from utils.data_reader import read_product_filters
from utils.logger import test_logger
import allure
import time

config = load_config()
CSV_FILE_PATH = "test_data/product_filters.csv"

@pytest.mark.usefixtures("setup")
class TestParfum:
    @allure.feature("Parfum Page")
    @pytest.mark.parametrize("filters_dict", read_product_filters(CSV_FILE_PATH))
    def test_parfum_page_with_filters(self, filters_dict):
        test_logger.info("Opening Parfum Page")
        parfum_page = ParfumPage(self.driver)
        try:
            with allure.step("Navigate to Parfum Page"):
                parfum_page.open_url(config["url"])
                test_logger.info("URL Opened Successfully")
            with allure.step("Accept Cookies"):
                parfum_page.accept_cookies()
                test_logger.info("Accepted Cookies")
            with allure.step(f"Apply filters: {filters_dict}"):
                test_logger.info(f"Applying filter: {filters_dict}")
                parfum_page.select_multiple_filters(filters_dict)
                test_logger.info(f"Successfully applied filter: {filters_dict}")

        except Exception as e:
            screenshot_path = f"screenshots/test_failure_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            test_logger.error(f"Error in test_open_parfum_page: {e}")
            raise

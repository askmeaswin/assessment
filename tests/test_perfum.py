import pytest
from pages.perfum_page import ParfumPage
from utils.data_loader import load_config
from utils.data_reader import read_product_filters

config = load_config()
CSV_FILE_PATH = "test_data/product_filters.csv"

@pytest.mark.usefixtures("setup")
class TestParfum:
    @pytest.mark.parametrize("filters_dict", read_product_filters(CSV_FILE_PATH))
    def test_parfum_page_with_filters(self, filters_dict):
        """Test navigation to the Parfum page and apply product filters dynamically."""
        parfum_page = ParfumPage(self.driver)
        parfum_page.open_url(config["url"])
        parfum_page.accept_cookies()
        parfum_page.select_multiple_filters(filters_dict)
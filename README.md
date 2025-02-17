# Selenium-Pytest Automation Framework

## Introduction

The Selenium-Pytest automation framework is designed for robust, scalable, and efficient test automation for web applications. This document provides an overview of the framework, its components, and usage guidelines.

## Framework Architecture

### Key Components

- **Selenium WebDriver** – For UI automation and browser interactions.
- **Pytest** – For test execution, reporting, and parameterization.
- **Page Object Model (POM)** – For maintainable test scripts.
- **Data-Driven Testing** – Uses CSV files for dynamic test data.
- **Logging & Reporting** – Integrated with `pytest-html` and `loguru`.
- **Utility Modules** – For handling shadow DOM, explicit waits, and video recording.

### Directory Structure

```
project_root/
│── tests/               # Test scripts
│── pages/               # Page Object Model classes
│── utils/               # Utility functions
│── test_data/           # CSV files for data-driven testing
│── config/              # Configuration files (config.yaml)
│── reports/             # Test execution reports
│── conftest.py          # Pytest fixtures & setup
│── requirements.txt     # Dependencies
│── pytest.ini           # Pytest configuration
```

## Features

### Pytest Integration

- **Fixtures**: Setup and teardown handled in `conftest.py`.
- **Markers**: Grouping and filtering test cases.
- **Parameterization**: Uses `pytest.mark.parametrize` for data-driven testing.

### Page Object Model (POM)

Each web page is represented as a class in `pages/`. Example:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ParfumPage(BasePage):
    PRODUCT_SELECT = (By.XPATH, "//*[text()='{}']")
    PRODUCT_BY_VALUE = (By.XPATH, "//*[text()='{}']//ancestor::a[@role='checkbox']")

    def select_product_filter(self, filter_name, value):
        wait = WebDriverWait(self.driver, 10)
        filter_element = wait.until(EC.element_to_be_clickable((By.XPATH, self.PRODUCT_SELECT[1].format(filter_name))))
        filter_element.click()
        value_element = wait.until(EC.element_to_be_clickable((By.XPATH, self.PRODUCT_BY_VALUE[1].format(value))))
        value_element.click()
```

### Data-Driven Testing

Test data is stored in `test_data/`. Example CSV:

```
Filter Name,Value
Produktart,Eau de Cologne
Marke,perfume.sucks
Für Wen,Unisex
Geschenk für,Valentinstag
```

CSV Reader:

```python
import csv

def read_product_filters(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [(row[0], row[1]) for row in reader]
```

### Shadow DOM Handling

Elements inside a Shadow DOM require special handling:

```python
def find_element_in_shadow_root(driver, shadow_host, selector):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    return shadow_root.find_element_by_css_selector(selector)
```

### Video Recording of Tests

Implemented using OpenCV (`cv2`):

```python
import cv2

def start_video_recording(filename):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    return cv2.VideoWriter(filename, fourcc, 20.0, (800, 600))
```

## Test Execution

### Running Tests

Run all tests:

```bash
pytest --html=reports/report.html --self-contained-html
```

Run a specific test:

```bash
pytest tests/test_parfum.py
```

Run tests with markers:

```bash
pytest -m smoke
```

## Conclusion

This framework provides a modular and scalable approach to test automation using Selenium and Pytest. Future enhancements may include **Allure Reporting**, **CI/CD integration**, and **cloud execution on Selenium Grid**.


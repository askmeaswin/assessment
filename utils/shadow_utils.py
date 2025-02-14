from selenium.webdriver.remote.webelement import WebElement

def get_shadow_root(driver, element):
    """Executes JavaScript to retrieve the shadow root of an element."""
    return driver.execute_script("return arguments[0].shadowRoot", element)

def find_element_in_shadow_root(driver, shadow_host, selector):
    """Finds an element inside a Shadow DOM using JavaScript."""
    return driver.execute_script("return arguments[0].shadowRoot.querySelector(arguments[1])", shadow_host, selector)
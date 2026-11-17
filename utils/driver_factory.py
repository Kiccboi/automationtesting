from selenium import webdriver

def launch_browser(browser: str="chrome",headless: bool=False):
    browser = browser.lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,768")
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,768")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Unsupported browser, {browser}")
    driver.implicitly_wait(0)
    return driver
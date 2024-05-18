from selenium import webdriver


class SeleniumDriverManager:
    def __init__(self, browser: str, options=None):
        self.browser = browser.lower()
        self.options = options

    def create_driver(self):
        if self.browser == 'chrome':
            driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            driver = webdriver.Firefox()
        elif self.browser == 'edge':
            driver = webdriver.Edge()
        elif self.browser == 'safari':
            driver = webdriver.Safari()
        elif self.browser == 'firefox':
            driver = webdriver.ChromiumEdge()
        else:
            raise ValueError(f"Navegador no soportado: {self.browser}")

        return driver


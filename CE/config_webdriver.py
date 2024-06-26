import configparser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options


class DriverConfig:
    """Clase para configurar el headless."""    
    @staticmethod
    def config_headless():
        """Funcion para activar el modo headless de la ventana."""
        config = configparser.ConfigParser()
        config.read('config.ini')
        headless_mode = config.getboolean('settings', 'headless')
        print("headless mode: ", headless_mode)

        if headless_mode:
            driver_options = Options()
            driver_options.add_argument('--headless')
            driver_options.add_argument('--no-sandbox')
            options = driver_options
            return options
        else:
            options = ""
            print("Corriendo con ventana del driver")
            return options
    
    @staticmethod
    def config_headless_chrome():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-breakpad')
        chrome_options.add_argument('--disable-component-extensions-with-background-pages')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        options = chrome_options

        return options

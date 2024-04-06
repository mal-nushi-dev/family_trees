import time
import configparser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


config = configparser.ConfigParser()
config.read('config.ini')


class FamilyEchoDownloader:
    """
    Automates the process of downloading family tree data from FamilyEcho
    using Selenium WebDriver.

    This class encapsulates the steps required to sign into FamilyEcho,
    navigate to the appropriate page, and trigger the download of the
    family tree data in CSV format. It's designed to run in a headless Chrome
    browser session for efficiency and can be customized
    via the `config.ini` file.

    Attributes:
    -----------
    url (str): The URL to start the automation process,
               typically the login page.
    username (str): The username for login.
    password (str): The password for login.
    driver (selenium.webdriver.Chrome): The Selenium WebDriver instance
                                        used for browser automation.
    wait (selenium.webdriver.support.ui.WebDriverWait): A WebDriverWait
        instance for managing dynamic content loading.

    Usage:
    ------
    >>> downloader = FamilyEchoDownloader(username='your_username',
    ...     password='your_password', url='login_page_url')
    >>> downloader.run()

    Note that this class is designed for use with Chrome WebDriver.
    Ensure you have ChromeDriver installed and
    accessible in your system's PATH.
    """
    SIGN_IN_ID = "do_signin"
    LOGIN_TYPE = "newuser_off"
    USERNAME = "username"
    PASSWORD = "password"
    LOGIN = "signinbutton"
    DOWNLOAD_PAGE = "//a[@title='Download/export family']"
    DOWNLOAD_OPTIONS = "extraframe"
    CSV_OPTION = "csv"
    DOWNLOAD_BUTTON = "do_download"

    def __init__(self, username: str, password: str, url: str) -> None:
        self.username = username
        self.password = password
        self.url = url
        self.driver = None
        self.wait = None

    def setup_driver(self) -> None:
        """
        Initializes the Selenium WebDriver with ChromeOptions for
        headless operation and other performance optimizations.

        This method configures the WebDriver to run Chrome in headless mode
        to improve performance and reduce resource usage during the automation
        process. Image loading is disabled to speed up page loads.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1200x600')
        # Do not load images automatically -- only concerned with texts
        image_preferences = {
            "profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", image_preferences)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 1)

    def sign_in(self) -> None:
        """
        Automates the sign-in process using the provided username and password.

        This method navigates through the sign-in form, inputs the username
        and password, and submits the form to log into the website.
        """
        print("Signing in...")
        sign_in_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, self.SIGN_IN_ID)))
        sign_in_button.click()

        login_type = self.driver.find_element(By.ID, self.LOGIN_TYPE)
        login_type.click()

        print("Inputting username...")
        username_input = self.driver.find_element(By.ID, self.USERNAME)
        username_input.clear()
        username_input.send_keys(self.username)

        print("Inputting password...")
        password_input = self.driver.find_element(By.NAME, self.PASSWORD)
        password_input.clear()
        password_input.send_keys(self.password)

        print("Logging in...")
        login = self.driver.find_element(By.ID, self.LOGIN)
        login.click()
        print("Successfully logged in!")

    def download_file(self) -> None:
        """
        Navigates to the download page and initiates the download of the
        family tree data in CSV format.

        This method waits for the download page link to become clickable,
        navigates to the download options, selects the CSV format, and clicks
        the download button. It waits for the download to
        initiate before proceeding.
        """
        print("Downloading file...")
        download_page = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.DOWNLOAD_PAGE)))
        download_page.click()
        time.sleep(5)

        download_options = self.driver.find_element(
            By.ID, self.DOWNLOAD_OPTIONS)

        # Point into iframe
        self.driver.switch_to.frame(download_options)

        csv_option = self.driver.find_element(By.ID, self.CSV_OPTION)
        csv_option.click()

        download_button = self.driver.find_element(
            By.NAME, self.DOWNLOAD_BUTTON)
        download_button.click()

        # Get out of iframe
        self.driver.switch_to.default_content()
        time.sleep(5)
        print("File successfully downloaded!")

    def run(self) -> None:
        """
        Executes the complete process of downloading the family tree
        data from FamilyEcho.

        This method orchestrates the setup of the WebDriver, signing in,
        navigating to the download page, and initiating the file download.
        It handles exceptions gracefully and ensures the WebDriver is
        properly closed after the operation.
        """
        try:
            self.setup_driver()
            self.driver.get(self.url)
            self.sign_in()
            self.download_file()
        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            self.driver.quit()

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
    A class used to automate the process of downloading family tree data
        from FamilyEcho.

    This class uses Selenium WebDriver to automate browser actions, including
        signing in to the website and navigating to the correct
        page to download the data.

    Attributes
    ----------
    URL : str
        The URL of the page to download data from.
    SIGN_IN_ID : str
        The HTML ID of the sign-in button on the page.
    LOGIN_TYPE : str
        The HTML ID of the login type radio button on the page.
    USERNAME : str
        The HTML ID of the username input field on the page.
    PASSWORD : str
        The HTML ID of the password input field on the page.
    LOGIN : str
        The HTML ID of the login button on the page.
    DOWNLOAD_PAGE : str
        The XPath of the download page link on the page.
    DOWNLOAD_OPTIONS : str
        The HTML ID of the iframe containing the download options on the page.
    CSV_OPTION : str
        The HTML ID of the CSV download option on the page.
    DOWNLOAD_BUTTON : str
        The HTML ID of the download button on the page.
    username : str
        The username to use to sign in to FamilyEcho.
    password : str
        The password to use to sign in to FamilyEcho.

    Methods
    -------
    setup_driver():
        Sets up the Selenium WebDriver with the necessary options.
    sign_in():
        Signs into the website using the provided username and password.
    download_file():
        Downloads the family tree file in CSV format.
    run():
        Runs the entire process of setting up the driver, signing in, and
            downloading the file.
    """
    URL = 'https://www.familyecho.com/?p=START&c=86mj7dkg5uovc9o3&f=746270266482117578'
    SIGN_IN_ID = "do_signin"
    LOGIN_TYPE = "newuser_off"
    USERNAME = "username"
    PASSWORD = "password"
    LOGIN = "signinbutton"
    DOWNLOAD_PAGE = "//a[@title='Download/export family']"
    DOWNLOAD_OPTIONS = "extraframe"
    CSV_OPTION = "csv"
    DOWNLOAD_BUTTON = "do_download"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """
        Sets up the Selenium WebDriver with the necessary options.
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

    def sign_in(self):
        """
        Signs into the website using the provided username and password.
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

    def download_file(self):
        """
        Downloads the family tree file in CSV format.
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

    def run(self):
        """
        Runs the entire process of setting up the driver, signing in,
            and downloading the file.
        Handles any exceptions that occur during the process.
        """
        try:
            self.setup_driver()
            self.driver.get(self.URL)
            self.sign_in()
            self.download_file()
        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            self.driver.quit()

import pytest
from selenium import webdriver
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

#Fixture for Chrome, Firefox, Edge
#@pytest.fixture(params=["Edge"],scope="class")
@pytest.fixture(params=["chrome", "Firefox"],scope="class")
def driver_init(request):
    if request.param == "chrome":
        opt = webdriver.ChromeOptions()
        opt.headless = True
        opt.add_argument('--no-sandbox')
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument('--disable-gpu')
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
    if request.param == "Firefox":
        opt = webdriver.FirefoxOptions()
        opt.headless = True
        opt.add_argument('--disable-gpu')
        web_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=opt)
    if request.param == "Edge":
        web_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.mark.usefixtures("driver_init")
class Test:
    pass


website = 'https://dabestteam.sitict.net'
class Test_GUI(Test):

        def test_WebsiteAliveDead(self):
            self.driver.get(website + "/")
            sleep(3)
            assert self.driver.title == "Let's Bid"

        def test_LoginNoReCaptcha(self):
            self.driver.get(website + "/login")
            sleep(3)
            self.driver.find_element(By.ID, 'email').send_keys('Derricktoh51@gmail.com')
            self.driver.find_element(By.ID, 'password').send_keys('blahblahblah')
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.NAME, 'Login'))
            sleep(5)
            assert self.driver.title == 'Login'
            assert 'Please fill out the ReCaptcha.' in self.driver.page_source

        def test_CreateAccEmailMismatch(self):
            self.driver.get(website + "/create_account")
            sleep(5)
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys('ing')
            self.driver.find_element(By.ID, 'email').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'confirmEmail').send_keys("Test123@gmail.com")
            self.driver.find_element(By.ID, 'displayName').send_keys("test User")
            self.driver.find_element(By.ID, 'mobileNumber').send_keys("91234567")
            self.driver.execute_script("arguments[0].value = '2000-01-01'", self.driver.find_element(By.ID, 'dob'))
            self.driver.find_element(By.ID, "mailingAddress").send_keys("Blk 123 ABC Road")
            self.driver.find_element(By.ID, "password").send_keys("123!@#asd321")
            self.driver.find_element(By.ID, "confirmPassword").send_keys("123!@#asd321")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'register'))
            sleep(5)
            assert self.driver.title == "Create Account"
            assert "Email mismatch. Please try again." in self.driver.page_source

        def test_CreateAccPasswordMismatch(self):
            self.driver.get(website + "/create_account")
            sleep(5)
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys('ing')
            self.driver.find_element(By.ID, 'email').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'confirmEmail').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'displayName').send_keys("test User")
            self.driver.find_element(By.ID, 'mobileNumber').send_keys("91234567")
            self.driver.execute_script("arguments[0].value = '2000-01-01'", self.driver.find_element(By.ID, 'dob'))
            self.driver.find_element(By.ID, "mailingAddress").send_keys("Blk 123 ABC Road")
            self.driver.find_element(By.ID, "password").send_keys("123!@#asd321")
            self.driver.find_element(By.ID, "confirmPassword").send_keys("123123123")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'register'))
            sleep(5)
            assert self.driver.title == "Create Account"
            assert "Password mismatch. Please try again." in self.driver.page_source       

        def test_CreateAccFutureDOB(self):
            self.driver.get(website + "/create_account")
            sleep(5)
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys('ing')
            self.driver.find_element(By.ID, 'email').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'confirmEmail').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'displayName').send_keys("test User")
            self.driver.find_element(By.ID, 'mobileNumber').send_keys("91234567")
            self.driver.execute_script("arguments[0].value = '2099-01-01'", self.driver.find_element(By.ID, 'dob'))
            self.driver.find_element(By.ID, "mailingAddress").send_keys("Blk 123 ABC Road")
            self.driver.find_element(By.ID, "password").send_keys("123!@#asd321")
            self.driver.find_element(By.ID, "confirmPassword").send_keys("123!@#asd321")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'register'))
            sleep(5)
            assert self.driver.title == "Create Account"
            assert "You cannot enter future date." in self.driver.page_source   
        
        def test_CreateAccDOBBelow21(self):
            self.driver.get(website + "/create_account")
            sleep(5)
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys('ing')
            self.driver.find_element(By.ID, 'email').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'confirmEmail').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'displayName').send_keys("test User")
            self.driver.find_element(By.ID, 'mobileNumber').send_keys("91234567")
            self.driver.execute_script("arguments[0].value = '2021-01-01'", self.driver.find_element(By.ID, 'dob'))
            self.driver.find_element(By.ID, "mailingAddress").send_keys("Blk 123 ABC Road")
            self.driver.find_element(By.ID, "password").send_keys("123!@#asd321")
            self.driver.find_element(By.ID, "confirmPassword").send_keys("123!@#asd321")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'register'))
            sleep(5)
            assert self.driver.title == "Create Account"
            assert "You must be 21 and above to register." in self.driver.page_source  

        def test_CreateAccCommonPassword(self):
            self.driver.get(website + "/create_account")
            sleep(5)
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys('ing')
            self.driver.find_element(By.ID, 'email').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'confirmEmail').send_keys("Test@gmail.com")
            self.driver.find_element(By.ID, 'displayName').send_keys("test User")
            self.driver.find_element(By.ID, 'mobileNumber').send_keys("91234567")
            self.driver.execute_script("arguments[0].value = '2000-01-01'", self.driver.find_element(By.ID, 'dob'))
            self.driver.find_element(By.ID, "mailingAddress").send_keys("Blk 123 ABC Road")
            self.driver.find_element(By.ID, "password").send_keys("123123123")
            self.driver.find_element(By.ID, "confirmPassword").send_keys("123123123")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.ID, 'register'))
            sleep(5)
            assert self.driver.title == "Create Account"
            assert "Password used is too common." in self.driver.page_source  
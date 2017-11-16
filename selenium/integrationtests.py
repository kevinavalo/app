import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import random
import string
from selenium.webdriver.support.select import Select

class RegisterTests(unittest.TestCase):
 
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
 
    def test_render_register(self):
        self.driver.get("web:8000/register")
        src = self.driver.page_source

        sign_up_found = re.search(r'Sign Up', src)
        uname_field = self.driver.find_element_by_id('id_username')
        pwd_field = self.driver.find_element_by_id('id_password')
        first_name_field = self.driver.find_element_by_id('id_first_name')
        last_name_field = self.driver.find_element_by_id('id_last_name')
        email_field = self.driver.find_element_by_id('id_email')
        phone_field = self.driver.find_element_by_id('id_phone_number')
        city_field = self.driver.find_element_by_id('id_city')
        state_field = self.driver.find_element_by_id('id_state')
        self.assertNotEqual(uname_field, None)
        self.assertNotEqual(pwd_field, None)
        self.assertNotEqual(first_name_field, None)
        self.assertNotEqual(last_name_field, None)
        self.assertNotEqual(email_field,None)
        self.assertNotEqual(phone_field, None)
        self.assertNotEqual(city_field, None)
        self.assertNotEqual(state_field, None)
        self.assertNotEqual(sign_up_found, None)

    def test_empty_register(self):
        self.driver.get("web:8000/register")
        self.driver.find_element_by_id('Register').click()
        result = self.driver.page_source
        text_found = re.search(r'Sign Up', result)
        self.assertNotEqual(text_found, None)

    def test_valid_register(self):
        self.driver.get("web:8000/register")

        uname_elm = self.driver.find_element_by_id("id_username")
        uname_elm.clear()
        N = 8
        random_uname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        uname_elm.send_keys(random_uname)
        pwd_elm = self.driver.find_element_by_id("id_password")
        pwd_elm.clear()
        pwd_elm.send_keys('muffinman')
        first_name_elm = self.driver.find_element_by_id("id_first_name")
        first_name_elm.clear()
        first_name_elm.send_keys('test')
        last_name_elm = self.driver.find_element_by_id("id_last_name")
        last_name_elm.clear()
        last_name_elm.send_keys('user')
        email_elm = self.driver.find_element_by_id("id_email")
        email_elm.clear()
        email_elm.send_keys('test@user.com')
        phone_elm = self.driver.find_element_by_id("id_phone_number")
        phone_elm.clear()
        phone_elm.send_keys('9739021684')
        city_elm = self.driver.find_element_by_id("id_city")
        city_elm.clear()
        city_elm.send_keys('Charlottesville')
        state_elm = self.driver.find_element_by_id("id_state")
        select = Select(state_elm)
        random_option = random.choice(select.options)
        state_elm.click()
        random_option.click()
        self.driver.find_element_by_id('Register').click()

        result = self.driver.page_source

        sign_up_found = re.search(r'Sign Up', result)
        feed_found = re.search(r'Welcome', result)
        self.assertEqual(sign_up_found,None)
        self.assertNotEqual(feed_found, None)


    def test_duplicate_uname_register(self):
        self.driver.get("web:8000/register")
        
        uname_elm = self.driver.find_element_by_id("id_username")
        uname_elm.clear()
        uname_elm.send_keys("rach")
        pwd_elm = self.driver.find_element_by_id("id_password")
        pwd_elm.clear()
        pwd_elm.send_keys('muffinman')
        first_name_elm = self.driver.find_element_by_id("id_first_name")
        first_name_elm.clear()
        first_name_elm.send_keys('test')
        last_name_elm = self.driver.find_element_by_id("id_last_name")
        last_name_elm.clear()
        last_name_elm.send_keys('user')
        email_elm = self.driver.find_element_by_id("id_email")
        email_elm.clear()
        email_elm.send_keys('test@user.com')
        phone_elm = self.driver.find_element_by_id("id_phone_number")
        phone_elm.clear()
        phone_elm.send_keys('9739021684')
        city_elm = self.driver.find_element_by_id("id_city")
        city_elm.clear()
        city_elm.send_keys('Charlottesville')
        state_elm = self.driver.find_element_by_id("id_state")
        select = Select(state_elm)
        random_option = random.choice(select.options)
        state_elm.click()
        random_option.click()
        self.driver.find_element_by_id('Register').click()

        result = self.driver.page_source
        sign_up_found = re.search(r'Sign Up', result)
        error_found = re.search(r'username taken',result)
        self.assertNotEqual(sign_up_found, None)
        self.assertNotEqual(error_found, None)


    def test_invalid_email_register(self):
        self.driver.get("web:8000/register")
        
        uname_elm = self.driver.find_element_by_id("id_username")
        uname_elm.clear()
        N = 8
        random_uname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        uname_elm.send_keys(random_uname)
        pwd_elm = self.driver.find_element_by_id("id_password")
        pwd_elm.clear()
        pwd_elm.send_keys('muffinman')
        first_name_elm = self.driver.find_element_by_id("id_first_name")
        first_name_elm.clear()
        first_name_elm.send_keys('test')
        last_name_elm = self.driver.find_element_by_id("id_last_name")
        last_name_elm.clear()
        last_name_elm.send_keys('user')
        email_elm = self.driver.find_element_by_id("id_email")
        email_elm.clear()
        email_elm.send_keys('test')
        phone_elm = self.driver.find_element_by_id("id_phone_number")
        phone_elm.clear()
        phone_elm.send_keys('9739021684')
        city_elm = self.driver.find_element_by_id("id_city")
        city_elm.clear()
        city_elm.send_keys('Charlottesville')
        state_elm = self.driver.find_element_by_id("id_state")
        select = Select(state_elm)
        random_option = random.choice(select.options)
        state_elm.click()
        random_option.click()

        self.driver.find_element_by_id('Register').click()

        result = self.driver.page_source
        text_found = re.search(r'Sign Up', result)
        self.assertNotEqual(text_found, None)

    def test_invalid_phone_register(self):
        self.driver.get("web:8000/register")
        
        uname_elm = self.driver.find_element_by_id("id_username")
        uname_elm.clear()
        N = 8
        random_uname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        uname_elm.send_keys(random_uname)
        pwd_elm = self.driver.find_element_by_id("id_password")
        pwd_elm.clear()
        pwd_elm.send_keys('muffinman')
        first_name_elm = self.driver.find_element_by_id("id_first_name")
        first_name_elm.clear()
        first_name_elm.send_keys('test')
        last_name_elm = self.driver.find_element_by_id("id_last_name")
        last_name_elm.clear()
        last_name_elm.send_keys('user')
        email_elm = self.driver.find_element_by_id("id_email")
        email_elm.clear()
        email_elm.send_keys('test@user.com')
        phone_elm = self.driver.find_element_by_id("id_phone_number")
        phone_elm.clear()
        phone_elm.send_keys('badnumber')
        city_elm = self.driver.find_element_by_id("id_city")
        city_elm.clear()
        city_elm.send_keys('Charlottesville')
        state_elm = self.driver.find_element_by_id("id_state")
        select = Select(state_elm)
        random_option = random.choice(select.options)
        state_elm.click()
        random_option.click()

        self.driver.find_element_by_id('Register').click()
        result = self.driver.page_source
        text_found = re.search(r'Sign Up', result)
        error_found = re.search(r'Enter a valid phone number.',result)
        self.assertNotEqual(text_found, None)
        self.assertNotEqual(error_found, None)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from locators import LoginPageLocators as Login, SidebarLocators as Sidebar, EnrollmentPageLocators as Enroll
from config import BASE_URL, LOGIN_CREDENTIALS, TEST_DATA
import time
import random

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.maximize_window()

driver.get(BASE_URL)

# 🔐 Login
driver.find_element(*Login.USERNAME).send_keys(LOGIN_CREDENTIALS["username"])
driver.find_element(*Login.PASSWORD).send_keys(LOGIN_CREDENTIALS["password"])
driver.find_element(*Login.SUBMIT).click()

wait.until(EC.presence_of_element_located(Sidebar.MENU))

# 📂 Navigate to New Enrollment
wait.until(EC.element_to_be_clickable(Sidebar.PREPAID_POSTPAID)).click()
wait.until(EC.element_to_be_clickable(Sidebar.NEW_ENROLLMENT)).click()

# 📝 Fill Form Step 1
wait.until(EC.presence_of_element_located(Enroll.ZIP_INPUT)).send_keys(TEST_DATA["zip_code"])
wait.until(EC.element_to_be_clickable(Enroll.FIRST_NAME)).send_keys(TEST_DATA["first_name"])
driver.find_element(*Enroll.LAST_NAME).send_keys(TEST_DATA["last_name"])
driver.find_element(*Enroll.ADDRESS).send_keys(TEST_DATA["address"])
driver.find_element(*Enroll.MAIL_ADDRESS).send_keys(TEST_DATA["address"])

rand_int = random.randint(1000, 9999)
email = f"testuser{rand_int}{TEST_DATA['email_domain']}"
driver.find_element(*Enroll.EMAIL).send_keys(email)

driver.find_element(*Enroll.NEXT_BUTTON).click()

# 🚚 Select Shipment
select = Select(wait.until(EC.presence_of_element_located(Enroll.SHIPMENT_DROPDOWN)))
select.select_by_visible_text(TEST_DATA["shipment_option"])

# 📲 Port-in details
driver.find_element(*Enroll.PORT_NUMBER).send_keys(TEST_DATA["port_number"])
driver.find_element(*Enroll.ESIM_CHECKBOX).click()

# 🏢 Carrier selection
carrier_dropdown = wait.until(EC.presence_of_element_located(Enroll.CARRIER_DROPDOWN))
select = Select(carrier_dropdown)
wait.until(lambda d: len(select.options) > 1)
select.select_by_index(1)  # Selecting second option as example

# 💻 Device ID
driver.find_element(*Enroll.DEVICE_ID).send_keys(TEST_DATA["device_id"])

# 🏠 Street Type
driver.find_element(*Enroll.STREET_TYPE).send_keys(TEST_DATA["street_type"])

# 🗂️ Account details
driver.find_element(*Enroll.ACCOUNT_NO).send_keys(TEST_DATA["account_no"])
driver.find_element(*Enroll.ACCOUNT_PASS).send_keys(TEST_DATA["account_pass"])

# ✅ Submit forms
driver.find_element(*Enroll.SUBMIT_FORM).click()
driver.find_element(*Enroll.PAYMENT_METHOD_SKIP).click()
wait.until(EC.visibility_of_element_located(Enroll.FINAL_SUBMIT)).click()



print("✅ Form filled successfully!")

time.sleep(5)
driver.quit()

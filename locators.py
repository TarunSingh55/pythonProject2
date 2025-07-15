from selenium.webdriver.common.by import By

class LoginPageLocators:
    USERNAME = (By.NAME, "login_user_id")
    PASSWORD = (By.NAME, "passwd")
    SUBMIT = (By.ID, "submit_button")

class SidebarLocators:
    MENU = (By.CLASS_NAME, "sidebar-menu")
    PREPAID_POSTPAID = (By.XPATH, "//span[contains(text(), 'Prepaid/postpaid orders')]")
    NEW_ENROLLMENT = (By.XPATH, "//a[contains(@href, 'enrollment_nll_step1')]")

class EnrollmentPageLocators:
    ZIP_INPUT = (By.NAME, "zip_code")
    FIRST_NAME = (By.ID, "fname")
    LAST_NAME = (By.ID, "lastname")
    ADDRESS = (By.NAME, "trad_address_main")
    MAIL_ADDRESS = (By.NAME, "un_d_address_main")
    EMAIL = (By.ID, "email")
    NEXT_BUTTON = (By.ID, "submit1")
    SHIPMENT_DROPDOWN = (By.XPATH, "//select[contains(@id, 'shipment_method')]")
    PORT_NUMBER = (By.XPATH, "//input[contains(@id, 'porting_number')]")
    ESIM_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and contains(@id, 'is_ESIM')]")
    CARRIER_DROPDOWN = (By.XPATH, "//select[starts-with(@id, 'carrier_')]")
    DEVICE_ID = (By.CSS_SELECTOR, ".form-control.device_cls")
    STREET_TYPE = (By.NAME, "porting_st_type[]")
    ACCOUNT_NO = (By.NAME, "porting_ac_number[]")
    ACCOUNT_PASS = (By.NAME, "account_pass[]")
    SUBMIT_FORM = (By.NAME, "submit")
    PAYMENT_METHOD_SKIP = (By.ID, "pay_method_3")
    FINAL_SUBMIT = (By.ID, "sub_cash")

    # ➡️ Carrier options xpaths
    CARRIER_OPTIONS_XPATHS = [
        "/html/body/div[3]/div[2]/section/div/div/div/div/div/div[2]/div/form/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/select/option[2]",
        "/html/body/div[3]/div[2]/section/div/div/div/div/div/div[2]/div/form/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/select/option[3]",
        "/html/body/div[3]/div[2]/section/div/div/div/div/div/div[2]/div/form/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/select/option[4]",
        # Add more as needed
    ]
